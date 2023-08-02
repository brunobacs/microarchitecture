import memory
from array import array

#Como precisamos aumentar as intrucoes pra 35 bits, aumentamos os numeros aceitos pelo firmware para Q = inteiro sem sinal de 64bits
firmware = array('Q', [0]) * 512

# main: PC <- PC + 1; MBR <- read_byte(PC); goto MBR
firmware[0] = 0b000000000_100_00_110101_001000_001_000001

# X = X + memory[address]
  ## 2: PC <- PC + 1; fetch; goto 3
firmware[2] = 0b000000011_000_00_110101_001000_001_000001
  ## 3: MAR <- MBR; read_word(MAR); goto 4
firmware[3] = 0b000000100_000_00_010100_100000_010_000010
  ## 4: X <- X + MDR;
firmware[4] = 0b000000000_000_00_111100_000100_000_000011

# X = X - memory[address]
  ## 5: PC <- PC + 1; fetch; goto 7
firmware[5] = 0b000000110_000_00_110101_001000_001_000001
  ## 6: MAR <- MBR; read; goto 9
firmware[6] = 0b000000111_000_00_010100_100000_010_000010
  ## 7: X <- X - MAR; goto 0
firmware[7] = 0b000000000_000_00_111111_000100_000_000011

# mov : memory[address] = X
  ## 8: PC <- PC + 1; fetch; goto 9
firmware[8] = 0b00001001_000_00_110101_001000_001_000001
  ## 9: MAR <- MBR; goto 10
firmware[9] = 0b00001010_000_00_010100_100000_000_000010
  ## 10: MDR <- X; write; goto 0
firmware[10] = 0b00000000_000_00_010100_010000_100_000011

# goto address
  ## 11: PC <- PC + 1; fetch; goto 12
firmware[11] = 0b00001100_000_00_110101_001000_001_000001
  ## 12: PC <- MBR; fetch; goto MBR
firmware[12] = 0b00000000_100_00_010100_001000_001_000010

# jz: if X == 0 goto address
  ## 13: X <- X; if alu = 0 goto 270 else goto 14
firmware[13] = 0b00001110_001_00_010100_000100_000_000011
  ## 14: PC <- PC + 1; goto 0
firmware[14] = 0b000000000_000_00_110101_001000_000_000001
  ## goto 270


# X = X * MEM[ADDRESS]
  ## PC <- PC + 1; fetch; GOTO 18
firmware[15] =  0b00010000_000_00_110101_001000_001_000001
  ## MAR <- MBR; MDR <- memory[MAR]; GOTO 19
firmware[16] =  0b00010001_000_00_010100_100000_010_000010
  ## X <- H * X; GOTO 0
firmware[17] =  0b000000000_000_00_101100_000100_000_000011

# JAM N if x == 1 goto address 
## 18: X<- X if alu != 0 goto 16
firmware[18] = 0b00001110_010_00_010100_000100_000_000011

# Y = Y + memory[address]
  ## 19: PC <- PC + 1; fetch; goto 20
firmware[19] = 0b00010100_000_00_110101_001000_001_000001
  ## 20: MAR <- MBR; read_word(MAR); goto 21
firmware[20] = 0b00010101_000_00_010100_100000_010_000010
  ## 21: Y <- Y + MDR; goto 0
firmware[21] = 0b00000000_000_00_111100_000010_000_000100

#Mov y, r
# mov : memory[address] = Y
  ## 24: PC <- PC + 1; fetch; goto 25
firmware[24] = 0b00011001_000_00_110101_001000_001_000001
  ## 25: MAR <- MBR; goto 26
firmware[25] = 0b00011010_000_00_010100_100000_000_000010
  ## 26: MDR <- Y; write; goto 0
firmware[26] = 0b00000000_000_00_010100_010000_100_000100


# Y = Y - memory[address]
  ## 27: PC <- PC + 1; fetch; goto 28
firmware[27] = 0b00011100_000_00_110101_001000_001_000001
  ## 28: MAR <- MBR; read; goto 29
firmware[28] = 0b00011101_000_00_010100_100000_010_000010
  ## 29: Y <- Y - MAR; goto 0
firmware[29] = 0b000000000_000_00111111_000010_000_000100

# jz: if Y == 0 goto address
  ## 13: Y <- Y; if alu = 0 goto 270 else goto 31
firmware[30]= 0b000011111_001_00_010100_000010_000_000100
  ## 14: PC <- PC + 1; goto 0
firmware[31]= 0b000000000_000_00_110101_001000_000_000001
  ## goto 287 => goto 11
firmware[287]= 0b00001011_000_00_000000_000000_000_000000




# HALT - STOP
firmware[255] = 0b00000000_000_00_000000_000000_000_000000

## 272: goto 11
firmware[270] = 0b00001011_000_00_000000_000000_000_000000


MPC = 0
MIR = 0

MAR = 0
MDR = 0
PC = 0
MBR = 0
X = 0
Y = 0
H = 0

N = 0
Z = 1

BUS_A = 0
BUS_B = 0
BUS_C = 0

#com o acrescimo parametro de A, pretendemos economizar passos e ler registradores também no barramento A
def read_regs(reg_numA, reg_numB):

  global MDR, PC, MBR, X, Y, H, BUS_A, BUS_B

#Agora podemos tirar todas as operacoes do H e colocar o registrador diretamente no barramento A, economizando pelo menos 1 passo em cada instrucao que continha H <- REG1 + REG2
  if reg_numA == 0:
    BUS_A = MDR
  elif reg_numA == 1:
    BUS_A = PC
  elif reg_numA == 2:
    BUS_A = MBR
  elif reg_numA == 3:
    BUS_A = X
  elif reg_numA == 4:
    BUS_A = Y
  elif reg_numA == 5:
    BUS_A = H 
  else:
    BUS_A = 0

  if reg_numB == 0:
    BUS_B = MDR
  elif reg_numB == 1:
    BUS_B = PC
  elif reg_numB == 2:
    BUS_B = MBR
  elif reg_numB == 3:
    BUS_B = X
  elif reg_numB == 4:
    BUS_B = Y
  elif reg_numB == 5:
    BUS_B = H 
  else:
    BUS_B = 0


def write_regs(reg_bits):

  global MAR, BUS_C, MDR, PC, X, Y, H

  if reg_bits & 0b100000:
    MAR = BUS_C

  if reg_bits & 0b010000:
    MDR = BUS_C

  if reg_bits & 0b001000:
    PC = BUS_C

  if reg_bits & 0b000100:
    X = BUS_C

  if reg_bits & 0b000010:
    Y = BUS_C

  if reg_bits & 0b000001:
    H = BUS_C


def alu(control_bits):

  global BUS_A, BUS_B, BUS_C, N, Z

  a = BUS_A
  b = BUS_B
  o = 0

  shift_bits = control_bits & 0b11000000
  shift_bits = shift_bits >> 6

  control_bits = control_bits & 0b00111111

  if control_bits == 0b011000:
    o = a
  elif control_bits == 0b010100:
    o = b
  elif control_bits == 0b011010:
    o = ~a
    #substituimos o circuito ~B pelo multiplicador
  elif control_bits == 0b101100:
    o = (a * b)
  elif control_bits == 0b111100:
    o = a + b
  elif control_bits == 0b111101:
    o = a + b + 1
  elif control_bits == 0b111001:
    o = a + 1
  elif control_bits == 0b110101:
    o = b + 1
  elif control_bits == 0b111111:
    o = b - a
  elif control_bits == 0b110110:
    o = b - 1
  elif control_bits == 0b111011:
    o = -a
  elif control_bits == 0b001100:
    o = a & b
  elif control_bits == 0b011100:
    o = a | b
  elif control_bits == 0b010000:
    o = 0
  elif control_bits == 0b110001:
    o = 1
  elif control_bits == 0b110010:
    o = -1

  if o == 0:
    N = 0
    Z = 1
  else:
    N = 1
    Z = 0

  if shift_bits == 0b01:
    o = o << 1
  elif shift_bits == 0b10:
    o = o >> 1
  elif shift_bits == 0b11:
    o = o << 8

  BUS_C = o


def next_instruction(next, jam):

  global MPC, MBR, N, Z

  if jam == 0b000:
    MPC = next
    return

  if jam & 0b001:  # JAMZ
    next = next | (Z << 8)

  if jam & 0b010:  # JAMN
    next = next | (N << 8)

  if jam & 0b100:  # JMPC
    next = next | MBR

  MPC = next
0

def memory_io(mem_bits):

  global PC, MBR, MDR, MAR

  if mem_bits & 0b001:  # FETCH
    MBR = memory.read_byte(PC)

  if mem_bits & 0b010:  # READ
    MDR = memory.read_word(MAR)

  if mem_bits & 0b100:  # WRITE
    memory.write_word(MAR, MDR)


def step():

  global MIR, MPC

  MIR = firmware[MPC]

  if MIR == 0:
    return False
  
  ## Estamos com instrucoes de 35 bits = 3 a mais para leitura de registradores no barramento A e reduzir passos nas operacoes da ula. 
  ## NextAddress__J__Des_ULA_______C___Mem__A___B_
  ## 0b000000000_000_00__000000_000000_000_000_000

#Alteraçoes no read_regs para os dois parametros. Acrescentamos 3 bits a cada um dos shifts abaixo
  read_regs((MIR & 0b00000000000000000000000000000111000), (MIR & 0b00000000000000000000000000000000111))
  alu((MIR & 0b00000000000011111111000000000000000) >> 15) # +3
  write_regs((MIR & 0b00000000000000000000111111000000000) >> 9) # +3
  memory_io((MIR & 0b00000000000000000000000000111000000) >> 6) # +3
  next_instruction((MIR & 0b11111111100000000000000000000000000) >> 26, #+3
                   (MIR & 0b00000000011100000000000000000000000) >> 23) # +3

  return True

