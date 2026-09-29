# -*- coding: utf-8 -*-
"""Minimal ESRI shapefile + dbf reader (polygons only). No external deps."""
import struct
def read_shp(path):
    """Return list of shapes; each shape = list of rings; ring = list of (x,y)."""
    data=open(path,'rb').read()
    n=len(data); pos=100; shapes=[]
    while pos < n:
        _num, clen = struct.unpack('>ii', data[pos:pos+8]); pos+=8
        rec=data[pos:pos+clen*2]; pos+=clen*2
        typ=struct.unpack('<i', rec[0:4])[0]
        if typ not in (5,15,25):      # Polygon / PolygonZ / PolygonM
            shapes.append([]); continue
        nparts, npoints = struct.unpack('<ii', rec[36:44])
        parts=list(struct.unpack('<%di'%nparts, rec[44:44+4*nparts]))
        off=44+4*nparts
        pts=struct.unpack('<%dd'%(2*npoints), rec[off:off+16*npoints])
        rings=[]
        for i,s in enumerate(parts):
            e=parts[i+1] if i+1<nparts else npoints
            rings.append([(pts[2*j],pts[2*j+1]) for j in range(s,e)])
        shapes.append(rings)
    return shapes
def read_dbf(path):
    f=open(path,'rb'); hdr=f.read(32)
    nrec,hlen,rlen=struct.unpack('<Ihh',hdr[4:12])
    fields=[]
    while True:
        fd=f.read(32)
        if fd[0:1]in(b'\r',b''): break
        name=fd[0:11].split(b'\x00')[0].decode('latin-1')
        flen=fd[16]
        fields.append((name,flen))
    f.seek(hlen); out=[]
    for _ in range(nrec):
        rec=f.read(rlen)
        if not rec: break
        o=1; d={}
        for name,flen in fields:
            d[name]=rec[o:o+flen].decode('latin-1').strip(); o+=flen
        out.append(d)
    return out
def pip(x,y,ring):
    """ray casting point-in-ring"""
    inside=False; n=len(ring); j=n-1
    for i in range(n):
        xi,yi=ring[i]; xj,yj=ring[j]
        if ((yi>y)!=(yj>y)) and (x < (xj-xi)*(y-yi)/(yj-yi+1e-300)+xi): inside=not inside
        j=i
    return inside
def in_shape(x,y,rings):
    c=0
    for r in rings:
        if pip(x,y,r): c+=1
    return c%2==1
