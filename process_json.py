import json

nodeid = 0

class Int:
    value =0
    def set(self,v):
        self.value=v
    def get(self):
        return self.value
    def inc(self, v):
        self.value=self.value+v
        return self.value


def ifnode(id, label, x,y):
  str="{ id: \"%s\",\n"%(id)
  str=str+"   type: \"cond\", \n"
  str=str+"   data: { label: \"%s\" },\n"%(label)
  str=str+"    position: { x: %d, y: %d } \n"%(x.get(),y.get())
  str=str+"  }"
  str=str.replace(r'\n','\n')
  return str

def endifnode(id, x,y):
   str="{ id: \"%s\",\n"%(id)
   str=str+"   type: \"endif\", \n"
   str=str+"    position: { x: %d, y: %d } \n"%(x.get(),y.get())
   str=str+"  }"
   str=str.replace(r'\n','\n')
   return str

def CommandNode(id, label,x,y):
  str="{ id: \"%s\",\n"%(id)
  str=str+"   type: \"process\", \n"
  str=str+"   data: { label: \"%s\" },\n"%(label)
  str=str+"    position: { x: %d, y: %d } \n"%(x.get(),y.get())
  str=str+"  }"
  str=str.replace(r'\n','\n')
  return str

def InOutNode(id, label,desc,x,y):
  str="{ id: \"%s\",\n"%(id)
  str=str+"   type: \"inout\", \n"
  str=str+"   data: { label: `%s` ,\n"%(label)
  str=str+"    desc: `%s` },\n"%(desc)
  
  str=str+"    position: { x: %d, y: %d } \n"%(x.get(),y.get())
  str=str+"  }"
  str=str.replace(r'\n','\n')
  return str

def getText(o):
    l=[]
    for x in o['suffix']:
        l.append(x['text'])
    return ",".join(l)

def visit(o, x,y, parent=None):
    global nodeid
    stepy=40
    stepx=10
    isArray=type(o)==list
    if isArray:
        l=[]
        prev=parent
        for i in range(len(o)):
            p=o[i]
            subl1=visit(p,x,y, prev)
            y.inc(stepy/2)
            if type(subl1)==list:
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
            d.append(ifnode(nodeid,"cond1",x,y))
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
            d.append(endifnode(nodeid,x,y))
            nodeid=nodeid+1
            return d
        if type_=='Command':
            lbl=""
            if 'name' in o:
                if 'text' in o['name']:
                    lbl=o['name']['text']
                    if lbl=='echo':
                            lbl='echo '
                            node=(InOutNode(nodeid,lbl,getText(o),x,y))
                            y.inc(stepy/2)
                            nodeid=nodeid+1
                            return node
                    else:
                        node=(CommandNode(nodeid,lbl,x,y))
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
  str=",".join(v)
  print(str)
