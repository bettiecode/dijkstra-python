#imports
import random, math
from numpy import copy
from PIL import Image, ImageDraw, ImageFont

#modelling the graph
points=[]
pcount=15 #edit freely, but not recommended to set over 20, preformance/runtime is unoptimized, and it takes forever
for i in range(pcount):
    points.append(i)
nodes=[]
ncount=random.randint(1,int((pcount-1)*pcount/2))
for i in range(ncount):
    correct = False
    while not correct:
        node=[random.choice(points),random.choice(points)]
        if (node[0]<node[1])and(node not in nodes):
            nodes.append(node)
            correct=True
for item in nodes:
    item.append(random.randint(1,8))
jrny=[0,0]
while jrny[0]==jrny[1]:
    jrny=[random.choice(points),random.choice(points)]
if jrny[0]>jrny[1]:
    jrny[0],jrny[1]=jrny[1],jrny[0]
#functions for the path seeking loop
def done():
    for item in paths:
        if item[-1]!=jrny[1]:
            return False
    return True

def get_possible(p):
    result=[]
    for item in nodes:
        if item[0]==p: result.append(item[1])
        if item[1]==p: result.append(item[0])
    return result

def repeats(pa):
    temp=[]
    for item in pa:
        if item in temp:
            return True
        else:
            temp.append(item)    
    return False

def impossible():
    for item in paths:
        poss=get_possible(item[-1])
        for jtem in poss:
            if jtem not in item: return False
    return True
#find paths
paths=[[jrny[0]]]
found=False
w=0

print(f"-finding paths(trough {len(nodes)} nodes)-")
while not done():
    if not found and impossible():
       paths=[]
       break 
    l=len(paths)
    for i in range(l):
        if paths[i][-1]!=jrny[1]:
            poss=get_possible(paths[i][-1])
            for j in range(len(poss)):
                path=paths[i].copy(); path.append(poss[j])
                paths.append(path)
    to_pop=[]
    for i in range(l):
        if paths[i][-1]!=jrny[1]:
            to_pop.append(paths[i])
    for item in to_pop:
        paths.remove(item)
    to_pop=[]
    for i in range(len(paths)):
        if (paths[i][-1]!=jrny[1]) and repeats(paths[i]):
            to_pop.append(paths[i])
    for item in to_pop:
        paths.remove(item)
    for item in paths:
        if item[-1]==jrny[1]:
            found=True
    print(w,len(paths),sep="  > ")
    w+=1
#count length
def get_node(s,e):
    for item in nodes:
        if s==item[0] and e==item[1]:   
            return item

totals=[]
for item in paths:
    d=0
    for i in range(len(item)-1):
        start=item[i]
        end=item[i+1]
        if start>end:
            start,end=end,start
        d+=get_node(start,end)[2]
    totals.append(d)
if found: 
    shortest=min(totals) 
    shortest_idxs=[]
    for i in range(len(totals)):
        if totals[i]==shortest: 
            shortest_idxs.append(i)

#visualizer functions
def ndconnect(nd):
    d0=math.radians(360*(nd[0]+1)/len(points))
    d1=math.radians(360*(nd[1]+1)/len(points))
    sp=(100*math.cos(d0)+128,100*math.sin(d0)+128)
    ep=(100*math.cos(d1)+128,100*math.sin(d1)+128)
    ImageDraw.Draw(img).line((sp,ep),"aqua",width=1)

def pmark(p):
    if p in jrny:
        color="green"
    else:
        color="red"
    d0=math.radians(360*(p+1)/len(points))
    sp=(100*math.cos(d0)+128,100*math.sin(d0)+128)
    ImageDraw.Draw(img).circle(sp,8,color)
    ImageDraw.Draw(img).text(sp,str(p),"blue",anchor="mm",font=font,stroke_width=0)
    

def ndmark(nd):
    d0=math.radians(360*(nd[0]+1)/len(points))
    d1=math.radians(360*(nd[1]+1)/len(points))
    sp=(100*math.cos(d0)+128,100*math.sin(d0)+128)
    ep=(100*math.cos(d1)+128,100*math.sin(d1)+128)
    d=4
    ImageDraw.Draw(img).text(((sp[0]+ep[0])/2,(sp[1]+ep[1])/2),str(nd[2]),"orange",anchor="mm",font=font,stroke_width=1)

def draw_path(pa):
    for i in range(len(pa)-1):
        d0=math.radians(360*(pa[i]+1)/len(points))
        d1=math.radians(360*(pa[i+1]+1)/len(points))
        sp=(100*math.cos(d0)+128,100*math.sin(d0)+128)
        ep=(100*math.cos(d1)+128,100*math.sin(d1)+128)
        ImageDraw.Draw(img).line((sp,ep),"purple",width=3)

#visualizing
img=Image.new("RGB",(256,256),"white")
font=ImageFont.truetype("arial.ttf",16)
for item in nodes:
    ndconnect(item)
if found: 
    for item in shortest_idxs:
        draw_path(paths[item])
for item in nodes:
    ndmark(item)
for item in points:
    pmark(item) 

img.save("dijkstra\djikstra.png")

#result report
print("-"*8)
print(f"nodes: {nodes}")
print(f"journey: {jrny}")
print("end results:")
if found:
    print(f"shorthest paths, with sum={shortest}:")
    for i in range(len(totals)):
        if totals[i]==shortest: print(paths[i])
else: print("no possible path")
print("-"*8)

