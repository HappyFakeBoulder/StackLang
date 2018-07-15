def textToNum(text): # pep8 says this should be text_to_bin, but you're using camelCase so I will too
  res = ""
  for char in text:
    assert(ord(char) < 256) # divToAscii only supports single-byte chars
    res += f"{ord(char):08b}" # binary ord padded to 8 bits
  return int(res, 2)
