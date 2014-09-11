def psalm_jar(lxx,mt):
  return str(lxx)+"::"+str(mt)+"::"

for n in range(1,151):
  if n == 9:
    print psalm_jar(n,n)
    print psalm_jar(n,n+1)
  elif (n >= 10 and n <= 112) or (n >= 116 and n <= 145):
    print psalm_jar(n, n+1)
  elif n == 113:
    print psalm_jar(n,n+1)
    print psalm_jar(n,n+2)
  elif n == 114 or n == 115:
    print psalm_jar(n,116)
  elif n == 146 or n == 147:
    print psalm_jar(n,147)
  else:
    print psalm_jar(n,n)
 
