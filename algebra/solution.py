from sympy import Eq, solveset, symbols, S, Interval
from sympy.parsing.sympy_parser import parse_expr
from pwn import remote, log

def parse(equation_text):
  lhs_text, rhs_text = equation_text.split('=')
  lhs = parse_expr(lhs_text, evaluate = False)
  rhs = parse_expr(rhs_text, evaluate = False)
  return Eq(lhs, rhs, evaluate = False)

def solve(equation):
  x = symbols('X')
  solutions = solveset(equation, x, domain = S.Reals).evalf()
  if isinstance(solutions, Interval):
    return 0
  else:
    return list(solutions)[0]

def main():
  HOST = 'misc.chal.csaw.io'
  PORT = 9002
  conn = remote(HOST, PORT)

  for i in range(7):
    log.info(conn.recvline().decode('utf-8'))

  p = log.progress('Working')
  while True:
    equation_text = conn.recvline(False).decode('utf-8')
    if equation_text.startswith('flag'):
      p.success(equation_text)
      break
    else:
      p.status(equation_text)
    conn.recvuntil('What does X equal?: ')
    equation = parse(equation_text)
    solution = solve(equation)
    conn.sendline(str(solution))
    line = conn.recvline(False).decode('utf-8')
    if line == 'YAAAAAY keep going':
      pass
    else:
      p.failure(line)
      raise Exception(line)
  conn.close()


TEST_EXPR_1 = '((((1 * X) * (14 - 14)) + ((14 + 9) + (14 * 3))) * (((10 * 6) * (17 + 14)) - ((6 - 12) * (10 * 18)))) + ((((7 + 11) + (20 + 2)) * ((2 - 18) * (14 * 5))) + (((9 + 20) - (18 * 3)) - ((2 - 20) * (1 + 13)))) = 146527'

TEST_EXPR_2 = '((((14 * X) - (14 + 1)) * ((3 * 10) - (4 * 13))) * (((12 + 5) * (19 + 7)) - ((4 + 5) * (17 - 5)))) * ((((18 + 17) + (20 + 16)) * ((14 - 14) * (10 * 20))) * (((6 * 6) * (13 - 3)) + ((2 - 11) * (3 * 8)))) = 0'

TEST_EXPR_3 = '(((((3 - 3) * (X * 1)) + ((15 * 15) + (14 - 8))) * (((11 * 2) + (11 * 15)) + ((2 + 20) - (6 + 12)))) * ((((3 + 1) + (2 - 19)) * ((7 * 15) - (7 - 14))) * (((19 * 16) * (6 + 7)) + ((11 + 4) - (12 + 19))))) + (((((7 - 4) + (8 + 6)) * ((18 + 1) * (9 + 7))) * (((19 * 5) - (18 * 11)) + ((18 * 20) - (17 - 17)))) + ((((7 * 8) * (16 * 20)) - ((20 + 16) + (1 * 2))) - (((13 + 5) + (10 + 11)) - ((7 + 7) + (3 + 5))))) = -252847986695'

main()
