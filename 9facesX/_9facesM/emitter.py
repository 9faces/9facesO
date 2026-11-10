from _9facesM.junk import JunkGenerator
from _9facesM.gates import Gates

class Emitter:
    def __init__(self, op, L2, chk1, chk2, seed):
        self.op = op; self.L2 = L2; self.chk1 = chk1; self.chk2 = chk2; self.seed = seed

    def _handler_bodies(self):
        op = self.op
        H = {
            "PUSH": "_H[{PUSH}]=function(ip) _ins(_S,_bc[ip+1]); return ip+2 end;",
            "ADD": "_H[{ADD}]=function(ip) local b=_rm(_S); local a=_rm(_S); _ins(_S,(a+b)%256); return ip+1 end;",
            "SUB": "_H[{SUB}]=function(ip) local b=_rm(_S); local a=_rm(_S); _ins(_S,(a-b)%256); return ip+1 end;",
            "MUL": "_H[{MUL}]=function(ip) local b=_rm(_S); local a=_rm(_S); _ins(_S,(a*b)%256); return ip+1 end;",
            "DIV": "_H[{DIV}]=function(ip) local b=_rm(_S); local a=_rm(_S); if b==0 then _ins(_S,0) else _ins(_S,math.floor(a/b)%256) end; return ip+1 end;",
            "MOD": "_H[{MOD}]=function(ip) local b=_rm(_S); local a=_rm(_S); if b==0 then _ins(_S,0) else _ins(_S,a%b) end; return ip+1 end;",
            "BXOR": "_H[{BXOR}]=function(ip) local b=_rm(_S); local a=_rm(_S); _ins(_S,_bx(a,b)); return ip+1 end;",
            "BAND": "_H[{BAND}]=function(ip) local b=_rm(_S); local a=_rm(_S); _ins(_S,_bd(a,b)); return ip+1 end;",
            "BOR": "_H[{BOR}]=function(ip) local b=_rm(_S); local a=_rm(_S); _ins(_S,bit32.bor(a,b)); return ip+1 end;",
            "BNOT": "_H[{BNOT}]=function(ip) local a=_rm(_S); _ins(_S,_bx(a,255)); return ip+1 end;",
            "CHR": "_H[{CHR}]=function(ip) local a=_rm(_S); if type(a)=='number' then _ins(_S,_char(math.floor(a)%256)) else _ins(_S,'') end; return ip+1 end;",
            "BYTE": "_H[{BYTE}]=function(ip) local a=_rm(_S); _ins(_S,_byte(a)); return ip+1 end;",
            "CAT": "_H[{CAT}]=function(ip) local s=_cat(_S); _S={s}; return ip+1 end;",
            "EXEC": "_H[{EXEC}]=function(ip) local s=_rm(_S); if type(s)=='string' then if type(_ld)=='function' then local ok,f=pcall(_ld,s); if not ok then warn('[9f] load: '..tostring(f)) elseif type(f)=='function' then local ok2,e2=pcall(f); if not ok2 then warn('[9f] runtime: '..tostring(e2)) end end end end; return -1 end;",
            "DUP": "_H[{DUP}]=function(ip) _ins(_S,_S[#_S]); return ip+1 end;",
            "POP": "_H[{POP}]=function(ip) _rm(_S); return ip+1 end;",
            "SWAP": "_H[{SWAP}]=function(ip) local n=#_S; if n>=2 then _S[n],_S[n-1]=_S[n-1],_S[n] end; return ip+1 end;",
            "JZ": "_H[{JZ}]=function(ip) local a=_rm(_S); if a==0 then return _bc[ip+1] else return ip+2 end end;",
            "JNZ": "_H[{JNZ}]=function(ip) local a=_rm(_S); if a~=0 then return _bc[ip+1] else return ip+2 end end;",
            "JMP": "_H[{JMP}]=function(ip) return _bc[ip+1] end;",
            "NOP": "_H[{NOP}]=function(ip) return ip+1 end;",
            "GLOAD": "_H[{GLOAD}]=function(ip) local k=_bc[ip+1]; _ins(_S,_G[k]); return ip+2 end;",
            "CALL": "_H[{CALL}]=function(ip) local n=_bc[ip+1]; local args={}; for i=1,n do args[n-i+1]=_rm(_S) end; local fn=_rm(_S); if type(fn)=='function' then _ins(_S,fn(unpack(args))) end; return ip+2 end;",
            "ROT": "_H[{ROT}]=function(ip) local n=#_S; if n>=3 then _S[n],_S[n-1],_S[n-2]=_S[n-2],_S[n],_S[n-1] end; return ip+1 end;",
            "OVER": "_H[{OVER}]=function(ip) local n=#_S; if n>=2 then _ins(_S,_S[n-1]) end; return ip+1 end;",
            "DROP2": "_H[{DROP2}]=function(ip) _rm(_S); _rm(_S); return ip+1 end;",
            "FAKE1": "_H[{FAKE1}]=function(ip) return ip+1 end;",
            "FAKE2": "_H[{FAKE2}]=function(ip) return ip+1 end;",
            "FAKE3": "_H[{FAKE3}]=function(ip) return ip+1 end;",
            "FAKE4": "_H[{FAKE4}]=function(ip) return ip+1 end;",
            "FAKE5": "_H[{FAKE5}]=function(ip) return ip+1 end;",
        }
        parts = []
        for name, tpl in H.items():
            parts.append(tpl.replace("{" + name + "}", str(op[name])))
        return " ".join(parts)

    def emit(self):
        arr = ",".join(str(x) for x in self.L2)
        junk = JunkGenerator.generate_inline(50)
        handlers = self._handler_bodies()
        gates = (f"local _c1=0; for _i=1,#_E do _c1=(_c1*31+_bd(_E[_i],255))%65536 end; "
                 f"if _c1 ~= {self.chk1} then return end; "
                 f"local _c2=0; for _i=1,#_E do _c2=(_c2+_E[_i])%100000 end; "
                 f"if _c2 ~= {self.chk2} then return end; ")
        init = (
            "local _char=string.char; local _byte=string.byte; "
            "local _cat=table.concat; local _ins=table.insert; local _rm=table.remove; "
            "local _bt=bit32; if not _bt then return end; "
            "local _bx=_bt.bxor; local _bd=_bt.band; "
            "local _ld=nil; pcall(function() if type(loadstring)=='function' then _ld=loadstring end end); "
            "if type(_ld)~='function' then pcall(function() local e=getfenv() if type(e)=='table' and type(e['loadstring'])=='function' then _ld=e['loadstring'] end end) end; "
            "if type(_ld)~='function' then return end; "
        )
        lua = (
            f"return(function(...) {junk} "
            f"{init} "
            f"local _E={{{arr}}}; "
            f"{gates}"
            f"local _L1={{}}; local _pv=0; for _i=1,#_E do _L1[_i]=_bx(_E[_i],_pv); _pv=_L1[_i]%256 end; "
            f"local _bc={{}}; for _i=1,#_L1 do _bc[_i]=_bx(_L1[_i],(_i*257+{self.seed})%65536) end; "
            f"local _H={{}}; local _S={{}}; "
            f"{handlers} "
            f"local _ip=1; local _steps=0; "
            f"while _ip>0 and _ip<=#_bc and _steps<500000 do _steps=_steps+1; local _h=_H[_bc[_ip]]; if _h then _ip=_h(_ip) else _ip=_ip+1 end end; "
            f"end)(...)"
        )
        return "-- [[ 9faces v1.5.4 ]] --\n-- [[ NO SKID~ :0 ]] --\n\n" + lua
