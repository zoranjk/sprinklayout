from objects import Map

FILELOC = "farmlands/meadowlands_sw_new.csv"
POP_SIZE = 1
INIT_SPRINKLERS = 17
SPRINKLER_TYPE = "iridiump"
INIT_SCARECROWS = 4
SCARECROW_TYPE = "normal"

if __name__ == "__main__":
    # initialize population ====================================================
    pop = []

    for _ in range(POP_SIZE):
        member = Map(FILELOC)
        
        for _ in range(INIT_SPRINKLERS):
            member.place_object(SPRINKLER_TYPE, member.rand_spot())

        for _ in range(INIT_SCARECROWS):
            member.place_object(SCARECROW_TYPE, member.rand_spot())

        pop.append(member)


    # evaluate
    
    for member in pop:
        member.print()
    
    
    # map = Map(FILELOC)
    
    
    # map.print()
    # map.place_object("iridiump", map.rand_spot())
    # map.place_object("iridiump", map.rand_spot())
    # map.place_object("iridiump", map.rand_spot())
    # map.place_object("iridiump", map.rand_spot())
    # map.place_object("iridiump", map.rand_spot())
    # map.place_object("iridiump", map.rand_spot())
    # map.place_object("normal", map.rand_spot())
    # # map.place_object("iridiump", (12,20))
    # # map.place_object("normal", (12,21))
    # map.print()