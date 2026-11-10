class Gates:
    @staticmethod
    def emit_gates(chk1, chk2):
        return (f"local _c1=0; for _i=1,#_E do _c1=(_c1*31+_bd(_E[_i],255))%65536 end; "
                f"warn('[9f dbg] chk1 got='.._c1..' expected={chk1}'); "
                f"if _c1 ~= {chk1} then warn('[9f GATE1 FAIL]'); return end; "
                f"local _c2=0; for _i=1,#_E do _c2=(_c2+_E[_i])%100000 end; "
                f"warn('[9f dbg] chk2 got='.._c2..' expected={chk2}'); "
                f"if _c2 ~= {chk2} then warn('[9f GATE2 FAIL]'); return end; "
                f"warn('[9f dbg] gates pass'); ")
