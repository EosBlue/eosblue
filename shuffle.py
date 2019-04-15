#-*—coding:utf8-*-
# used in contract eosbluejacks/eosbluethree/eosbluetexas/eosbluecarib
# server_seed and player_seed are used in eosbluejacks/eosbluethree/eosbluecarib
# server_seed and block_hash are used in eosbluetexas
# @Date    : 2019-4-15 10:40:03
# @Author  : eosblue

import json
import hashlib

"""
        A  2  3  4  5  6  7  8  9  10  J  Q  K
diamond 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,
heart   13,14,15,16,17,18,19,20,21,22,23,24,25,
spade   26,27,28,29,30,31,32,33,34,35,36,37,38,
club    39,40,41,42,43,44,45,46,47,48,49,50,51,
"""

"""
character to hex number
"""
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

if __name__ == '__main__':

    block_hash    = "03246dfdc310b823b785c45759224744b19f2cd6da02ed2c14d9c99981045e24"
    server_seed   = "6a4e7c1b225820d502444a74b01f8285"
    player_seed   = "0e08ca9aa18e3b7538d36917b6de5561"
    
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

    print "================================================================\n\
number to card:\n\
        A  2  3  4  5  6  7  8  9  10  J  Q  K\n\n\
diamond 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,\n\
heart   13,14,15,16,17,18,19,20,21,22,23,24,25,\n\
spade   26,27,28,29,30,31,32,33,34,35,36,37,38,\n\
club    39,40,41,42,43,44,45,46,47,48,49,50,51,"
    

    



