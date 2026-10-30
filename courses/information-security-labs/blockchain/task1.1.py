blocks=[]
for i in range(10):
    value =(i+1)*100
    blocks.append({"index": i, "data": [value]})
    
print(type(blocks))