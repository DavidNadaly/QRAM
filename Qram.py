#importing standard Qiskit libraries

import numpy as np
from qiskit import QuantumCircuit, transpile, Aer, IBMQ, 
QuantumRegister, ClassicalRegister, execute
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from ibm_quantum_widgets import *
from qiskit.providers.aer import QasmSimulator
from math import pi
# Loading your IBM Quantum account(s)
provider = IBMQ.load_account()

'''This is the circuit for 10 qubit QRAM, designed to upload only
two quantum states. The unitary gate in the circuit can be further 
modified to upload states of specific amplitude'''

quant_state_1 = str("1111001011")
quant_state_2 = str("1100100101")
#You can add any 10 bit quantum states

qr1 = QuantumRegister(2, name ='a')   
'''#Auxillary register. It is initialized to store 01 state. 
After uploading first quantum state the auxillary register  will exist
in  the state 00 and 01.  The  state with 00  will be entangled
with the quantum state stored in memory and the next state to 
be uploaded will be entangled with 01 state  of auxillary register.'''
qr2 = QuantumRegister(10, name = 'm')
#This is the memory  register where quant states are stored.
qc = QuantumCircuit(qr1,qr2,)
qc.x(qr1[1]) #Auxillary register initialized to 01 state


#memory_circuit is a fn. to store the bits in memory register
def memory_circuit(qc,quant_state):
    m = 0 #m=0 correspond to zeroth qubit in memory register
    for i in range(len(quant_state)-1,-1,-1):
        if (int(quant_state[i]) == 0): 
            qc.x(qr2[m]) 
            #X gate is applied if the state to be uploaded is 0
            m = m+1 '''During each iteration the gate is applied
            from 0th qubit to 1st qubit, 2nd, 3rd and so on.'''
        if (int(quant_state[i]) == 1):
            qc.cx(qr1[1],qr2[m]) '''CX gate is applied on  memory 
            register and auxillary register if the state to be 
            uploaded is 1. '''
            m = m+1
    return qc

#Desigining a gate to store the initial state with amplitude (1/sqrt(2))
def unitary_1():
    my_circuit = QuantumCircuit(1)
    my_circuit.z(0)
    my_circuit.ry(pi/2,0)
    my_circuit.z(0)
    my_gate = my_circuit.to_gate()
    my_gate.name = "ZRy(pi/2)Z"
    my_control_gate = my_gate.control()
    return my_control_gate

#Desigining a gate to store the second quantun state with amplitude (1/sqrt(2))
def unitary_2():
    my_circuit = QuantumCircuit(1)
    my_circuit.z(0)
    my_circuit.ry(pi,0)
    my_circuit.z(0)
    my_gate = my_circuit.to_gate()
    my_gate.name = "ZRy(pi)Z"
    my_control_gate = my_gate.control()
    return my_control_gate

#uplading 1st quantum state
memory_circuit(qc,quant_state_1) #calling memory_circuit function
qc.mct([qr2[0],qr2[1],qr2[2],qr2[3],qr2[4],qr2[5],qr2[6],qr2[7],qr2[8],qr2[9]],qr1[0])
#applying multicontrol gate, targeted on 0th qubit of auxillary registed controlled 
#by 10 qubits of memory register
qc.append(unitary_1(), [qr1[0]]+[qr1[1]]) #appending the unitary gate 
qc.mct([qr2[0],qr2[1],qr2[2],qr2[3],qr2[4],qr2[5],qr2[6],qr2[7],qr2[8],qr2[9]],qr1[0]) 
#calling multicontrol gate again
memory_circuit(qc,quant_state_1) #calling memory_circuit function again.
qc.barrier()

#uploading 2nd quantum  state
memory_circuit(qc,quant_state_2) #applying memory_circuit fn on memory register
qc.mct([qr2[0],qr2[1],qr2[2],qr2[3],qr2[4],qr2[5],qr2[6],qr2[7],qr2[8],qr2[9]],qr1[0]) 
'''applying multicontrol gate, targeted on 0th qubit of auxillary register 
controlled by 10 qubits of memory register'''
qc.append(unitary_2(), [qr1[0]]+[qr1[1]]) #appending unitary gate
qc.mct([qr2[0],qr2[1],qr2[2],qr2[3],qr2[4],qr2[5],qr2[6],qr2[7],qr2[8],qr2[9]],qr1[0]) 
#applying the same multicontrol gate again
memory_circuit(qc,quant_state_2) #calling memory_circuit function again
qc.barrier()
qc.draw()

#The state to be uploaded have now been uploaded and stored in memory register.
#By measuring the memory register, we can check whether the state was properly uploaded.
#To add quantum states of specific amplitude, unitary gates have to be designed accordingly
