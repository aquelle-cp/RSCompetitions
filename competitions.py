from logic import *

# Competition start
# current_xp = get_current_xp_all()
# store_xp_in_file(current_xp, 'slayer_1_start')

# Get current standings
start_xp = pull_xp_from_file('start-files/slayer_1_start')
start_xp = get_xp_one_skill(start_xp, SLAYER)
current_xp = get_current_xp_all()
current_xp = get_xp_one_skill(current_xp, SLAYER)
current_xp_gains = calc_xp_gained(start_xp, current_xp)
current_xp_gains = filter_no_xp_gained(current_xp_gains)
current_xp_gains = sorted(current_xp_gains, key=lambda l:l[1], reverse=True)
for i in range(len(current_xp_gains)):
    print(str(i + 1) + '.' + ' ' + current_xp_gains[i][0] + '\t' + str(current_xp_gains[i][1]))

# store_xp_in_file(current_xp, 'finish-files/thieving_1_finish')

# Get final standings
# start_xp = pull_xp_from_file('test_start')
# finish_xp = get_current_xp_all()
# store_xp_in_file(finish_xp, 'dg_1_finish')
# final_xp_gains_all = calc_xp_gained(start_xp, finish_xp)
# print(final_xp_gains_all)
