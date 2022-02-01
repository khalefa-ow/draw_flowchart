import json

nodeid = 0
edgeid=0
edges=[]

class edge:
  src=0
  dst=0

  def __init__(self, str, dst):
    self.src=src
    self.dst=dst
    global edgeid
    edgeid=edgeid+1

  def __str__(self):
    ss="{ id=e%d: }"%(self.edgeid)
    ss=ss+"source : %s"%(self.src)
    ss=ss+"dst : %s}"%(self.dst)
    return ss
def IfNode(id,  x,y, label):
  print("x"+str(x))
  print("y"+str(y))
  ss="{ id: \"%s\",\n"%(id)
  ss=ss+"   type: \"cond\", \n"
  ss=ss+"   data: { label: \"%s\" },\n"%(label)
  ss=ss+"    position: { x: %d, y: %d } \n"%(x,y)
  ss=ss+"  }"
  ss=ss.replace(r'\n','\n')
  return ss

def EndifNode(id, x,y):
   ss="{ id: \"%s\",\n"%(id)
   ss=ss+"   type: \"endif\", \n"
   ss=ss+"    position: { x: %d, y: %d } \n"%(x,y)
   ss=ss+"  }"
   ss=ss.replace(r'\n','\n')
   return ss

def CommandNode(id, x,y,label):
  ss="{ id: \"%s\",\n"%(id)
  ss=ss+"   type: \"process\", \n"
  ss=ss+"   data: { label: \"%s\" },\n"%(label)
  ss=ss+"    position: { x: %d, y: %d } \n"%(x,y)
  ss=ss+"  }"
  ss=ss.replace(r'\n','\n')
  return ss

def InOutNode(id,x,y, label,desc):
  ss="{ id: \"%s\",\n"%(id)
  ss=ss+"   type: \"inout\", \n"
  ss=ss+"   data: { label: `%s` ,\n"%(label)
  ss=ss+"    desc: `%s` },\n"%(desc)
  
  ss=ss+"    position: { x: %d, y: %d } \n"%(x,y)
  ss=ss+"  }"
  ss=ss.replace(r'\n','\n')
  return ss

def getText(o):
    l=[]
    for x in o['suffix']:
        l.append(x['text'])
    return ",".join(l)
class Int:
    value =0
    def set(self,v):
        self.value=v
    def get(self):
        return self.value
    def inc(self, v):
        self.value=self.value+v
        return self.value

class Node:
  x=0
  y=0
  nodetype=''
  id=0
  label=""
  desc=""

  def __init__(self, nodetype, id, x, y,label="", desc=""):
    self.id=id
    self.label=label
    self.desc=desc
    self.x=x.get()
    self.y=y.get()
    self.nodetype=nodetype

  def __str__(self): 
    if self.nodetype=='if':
        return IfNode(self.id,  self.x, self.y, self.label)
    elif self.nodetype =='endif':
        return EndifNode(self.id, self.x, self.y)
    elif self.nodetype== 'cmnd':
        return CommandNode(self.id,self.x,self.y,self.label)
    elif self.nodetype=='inout':
        return InOutNode(self.id, self.x, self.y, self.label, self.desc)
    else:
        return ''


def visit(o, x,y, parent=None):
    global nodeid
    stepy=40
    stepx=10
    isArray=type(o)==list
    if isArray:
        l=[]
        prev=parent
        prevnode=None
        for i in range(len(o)):
            p=o[i]
            subl1=visit(p,x,y, prev)
            y.inc(stepy/2)
            if type(subl1)==list:
                if len(l)>0:
                   prevnode=l[-1]
                   firstnode=subl1[0]
                   print(prevnode )
                   print(firstnode)
                l.extend(subl1)

            else:
                l.append(subl1)
            prev=o[i]
        return l
    else:
        isObject=type(o)==dict
        type_= o['type']
        if (type_=='Script') | (type_ =="CompoundList") | (type_== "Pipeline"):
            return visit(o['commands'],x,y, parent);
        if type_=='If':
            then_clause=None
            else_clause=None
            d=[]
            x_s=x.get()
            y_s=y.get()
            d.append(Node("if",nodeid,x,y,"cond1"))
            nodeid=nodeid+1

            xelse=Int()
            yelse=Int()
            xelse.set(x_s)
            yelse.set(y_s)


            if 'then' in o:
                then_clause=o['then']
                x.inc(stepx)
                y.inc(stepy/2)
                d.extend(visit(then_clause,x,y,o))
            if 'else' in o:
                else_clause=o['else']
                xelse.inc(-stepx)
                yelse.inc(stepy/2)

                d.extend(visit(else_clause,xelse, yelse,o))
            x.set(max(x.get(),xelse.get()))
            d.append(Node("endif",nodeid,x,y))
            nodeid=nodeid+1
            return d

        if type_=='Command':
            lbl=""
            if 'name' in o:
                if 'text' in o['name']:
                    lbl=o['name']['text']
                    if lbl=='echo':
                            lbl='echo '
                            node=(Node("inout",nodeid,x,y,lbl,getText(o)))
                            y.inc(stepy/2)
                            nodeid=nodeid+1
                            return node
                    else:
                        node=(Node("cmnd", nodeid,x,y, lbl))
                        y.inc(stepy/2)
                        nodeid=nodeid+1
                        return node
        return []


with open('terad.json', 'r') as f:
  data = json.load(f)
  x=Int()
  x.set(150)
  y=Int()
  y.set(30)

  v=(visit(data,x,y))
  l=[]
  for s in v:
      l.append(str(s))
  str=",".join(l)
  print(str)
