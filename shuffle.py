#-*—coding:utf8-*-
# used in contract eosbluejacks/eosbluethree/eosbluetexas/eosbluecarib
# server_seed and player_seed are used in eosbluejacks/eosbluethree/eosbluecarib
# server_seed and block_hash are used in eosbluetexas
# @Date    : 2019-4-15 10:40:03
# @Author  : eosblue

import json
import hashlib

'''
        A  2  3  4  5  6  7  8  9  10  J  Q  K
diamond 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,
heart   13,14,15,16,17,18,19,20,21,22,23,24,25,
spade   26,27,28,29,30,31,32,33,34,35,36,37,38,
club    39,40,41,42,43,44,45,46,47,48,49,50,51,
'''

'''
character to hex number, used in md5 or sha512 digest
'''
hex_dict = {
    '0':0,
    '1':1,
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    'a':10,
    'b':11,
    'c':12,
    'd':13,
    'e':14,
    'f':15    
}

'''
generate 6 cards in game Baccarat
@server_seed  : a md5 string
@block_hash   : block id of one appointed block int the next few seconds, we use the last 32 character of the block id
'''
def gen_baccarat_cards(server_seed, block_hash):
    if len(server_seed) != 32 or len(block_hash) != 64:
        return [], ''
    m = hashlib.md5()   
    m.update(str(server_seed) + str(block_hash[32:]))
    real_seed = m.hexdigest()
    first_md5 = real_seed
    # result cards
    cards = []
    while True:
        for i in range(32):
            c = hex_dict[real_seed[i]]
            if c <= 12:
                cards.append(c)
        if len(cards) < 6:
            m.update(real_seed)
            real_seed = m.hexdigest()
            continue
        break
    return cards[:6], first_md5

'''
generate lottery hit number, used in game Power Ball
@server_seed  : a md5 string
@block_hash   : block id of one appointed block int the next few minutes, we use the last 32 character of the block id
'''
def gen_lottery_number(server_seed, block_hash):
    if len(server_seed) != 32 or len(block_hash) != 64:
        return []
    block_seed = block_hash[32:]
    # lottery number
    white_number = []
    red_number = []
    result = []
    for i in range(32):
        if len(white_number) >= 4 and len(red_number) >= 1:
            break
        if len(white_number) < 4:
            c1 = hex_dict[server_seed[i]]
            c2 = hex_dict[block_seed[i]]
            n = ((c1 * 16 + c2) % 32) + 1
            if n in white_number:
                continue
            white_number.append(n)
        else:
            c1 = hex_dict[server_seed[i]]
            c2 = hex_dict[block_seed[i]]
            n = ((c1 * 16 + c2) % 16) + 1
            red_number.append(n)
    if len(white_number) != 4 or len(red_number) <= 0:
        return []
    result = white_number
    result.append(red_number[0])
    return result

'''
shuffle cards(0-51), used in game BlackJack, Threes, Texas Hold'em, Caribbean
'''
def shuffle_card(seed1, seed2):
    seed = str(seed1) + str(seed2)
    sha512_digest = hashlib.sha512(seed).hexdigest()
    if len(sha512_digest) != 128:
        return [], ''
    #number array(0-255), length may be less than 64
    seed_array = []
    for index in range(64):
        seed_num = hex_dict[sha512_digest[index * 2]] * 16 +  hex_dict[sha512_digest[index * 2 + 1]]
        # ignore the number greater than 207
        if seed_num < 52 * 4:
            seed_array.append(seed_num)
    # cards to be shuffled
    new_cards = [-1 for _ in range(52)]
    # seed index, increase 1 when shuffle one card, and back to 0 when it come to the end to seed_array
    seed_index = 0
    # start shuffle
    for card in range(52):
        # the new index in new_cards of card 
        card_index = seed_array[seed_index] % 52;
        if new_cards[card_index] == -1:
            new_cards[card_index] = card;
        # new index conflict, move all contiguous shuffled card to next position
        else:
            next_card = new_cards[card_index]
            new_cards[card_index] = card;
            tmp_index = card_index
            while next_card != -1:
                tmp_index = (tmp_index + 1) % 52
                tmp_card = new_cards[tmp_index]
                new_cards[tmp_index] = next_card
                next_card = tmp_card

        seed_index = (seed_index + 1) % len(seed_array)
    return new_cards, sha512_digest

def test_shuffle():
    block_hash    = "0329ebb1830db1a68efa0647e3b62d84a6eb008ea34dbec6096e4a2f10fb58ce"
    server_seed   = "dcc42f86c42f3b05d68348abbebdade4"
    player_seed   = "ffe1002240c20cb1ef3f528f895a4dcf"
    
    #shuffle cards use block_hash
    cards1, sha512_digest1 = shuffle_card(server_seed, player_seed)
    cards2, sha512_digest2 = shuffle_card(server_seed, block_hash[32:])
    
    print 'game seed:', server_seed
    print 'player seed:', player_seed
    print 'block hash:', block_hash
    print '================================================================\n'
    print 'sha512 by player seed:', sha512_digest1
    print 'shuffled cards by player seed:', cards1
    print '================================================================\n'
    print 'sha512 by block hash:', sha512_digest2
    print 'shuffled cards by block hash:', cards2

def test_baccarat():
    block_hash    = "0329e20dad88f57197afb3131421c6ad43732332a30d2d7e558d687c01036e69"
    server_seed   = "6c77b0687848dfb1e0c89c11ff6dace1"
    result, seed_md5 = gen_baccarat_cards(server_seed, block_hash)
    
    print '================================================================\n'
    print 'generate baccarat cards'
    print 'game seed:', server_seed
    print 'block hash:', block_hash
    print 'seed_md5:', seed_md5
    print 'baccarat result number:', result

def test_lottery():
    block_hash    = "03246dfdc310b823b785c45759224744b19f2cd6da02ed2c14d9c99981045e24"
    server_seed   = "6a4e7c1b225820d502444a74b01f8285"
    result = gen_lottery_number(server_seed, block_hash)

    print '================================================================\n'
    print 'generate lottery numbers'
    print 'game seed:', server_seed
    print 'block hash:', block_hash
    print 'lottery result number:', result

if __name__ == '__main__':

    test_shuffle()
    test_baccarat()
    test_lottery()

    print "================================================================\n\
number to card:\n\
        A  2  3  4  5  6  7  8  9  10  J  Q  K\n\n\
diamond 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,\n\
heart   13,14,15,16,17,18,19,20,21,22,23,24,25,\n\
spade   26,27,28,29,30,31,32,33,34,35,36,37,38,\n\
club    39,40,41,42,43,44,45,46,47,48,49,50,51,"
    

    



