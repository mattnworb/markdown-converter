#!/usr/bin/python

import re, os, sys



def convertText(c):
    # replace all links
    # c = re.sub(r'\[([^\]]+)\]\(([^\]]+)\)', r'[\1|\2]', c)
    c = re.sub(r'\[(.*?)\]\((.*?)\)', r'[\1|\2]', c)

    # replace bold temporarily
    c = re.sub(r'\*\*(.*?)\*\*', r'bdirkb\1bdirkb', c)
    # replace italics
    c = re.sub(r'\*(.*?)\*', r'_\1_', c)
    # replace bold
    c = re.sub(r'bdirkb(.*?)bdirkb', r'*\1*', c)

    # replace inline code
    c = re.sub(r'`(.*?)`', r'*\1*', c)

    # print c
    c = c.split('\n')

    words = []
    words.append( ['#','h1.'] )
    words.append( ['##','h2.'] )
    words.append( ['###','h3.'] )
    words.append( ['####','h4.'] )
    words.append( ['#####','h5.'] )
    words.append( ['######','h6.'] )

    newContent = []

    isCode = 0
    indent = 0
    isQuote = 0
    isList = 0

    for l in c:
      if 0 == 0:
        k = l
        if l[0:1]=='*':
          isList = 1
        if l == '':
          isList = 0

        if l[0:1] == '>':
          if isQuote==0:
            k = '{quote}\n'+k[1:]
            isQuote = 1
          else:
            k = k[1:]


        if isList == 0:
          if isCode == 1:
            if l[0:1] == ' ' or l[0:1]=='\t':
              k = k[indent:]  
            else:
              k = '{code}\n'+k
              isCode = 0
              indent = -1
          else:
            if l[0:1]==' ' or l[0:1]=='\t':
              indent = len(k)-len(k.lstrip())
              k = '{code}\n'+k[indent:]              
              isCode = 1
        else:
           if l[0:4]=='\t\t\t*':
             k = '****' + l[4:]
           if l[0:3]=='\t\t*':
             k = '***' + l[3:]
           if l[0:2]=='\t*':
             k = '**' + l[2:]

        for w in words:
          # print l[:len(w[0])]
          if l[:len(w[0])] == w[0]:
            k = w[1]+l[len(w[0]):]


        if l[0:1] != '>' and isQuote == 1:
          k = '{quote}\n'+k
          isQuote = 0


        if l[0:3] != '| -':
          newContent.append(k)

    return '\n'.join(newContent)


if __name__=='__main__':


    if len(sys.argv)<2:
        print "Usage: markdown_converter.py <input file>"
        sys.exit(1)

    infile = sys.argv[1]

    if not os.path.exists(infile):
        sys.stderr("%s does not exist!" %infile)
        sys.exit(15)

    with open(infile, 'r') as f:
        text = f.read()
        print convertText(text)


