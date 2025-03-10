# test_rankine.py
from rankine import rankine

def main():
    # Case 1: Saturated vapor entering the turbine
    rankine1 = rankine(p_low=8, p_high=8000, name='Rankine Cycle - Saturated Vapor')
    eff1 = rankine1.calc_efficiency()
    rankine1.print_summary()

    # Case 2: Superheated steam entering the turbine
    rankine2 = rankine(p_low=8, p_high=8000, t_high=500, name='Rankine Cycle - Superheated Steam')
    eff2 = rankine2.calc_efficiency()
    rankine2.print_summary()

if __name__ == "__main__":
    main()