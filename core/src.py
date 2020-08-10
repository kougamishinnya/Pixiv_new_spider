from interface import pixiv_interface

rank_mode_dict = {
    '1': ['Illust_mode', {
        '1': 'daily',
        '2': 'weekly',
        '3': 'monthly',
        '4': 'rookie',
    }],
    '2':
        ['All_mode',
         {'1': 'daily',
          '2': 'weekly',
          '3': 'monthly',
          '4': 'rookie',
          '5': 'male',
          '6': 'female', }]
}


# proxy = common.get_ips()

def rank_mode():
    global rank_mode_dict

    def check_dict(dict):
        print("=====   MODE   =====\n")
        for key, value in dict.items():
            print(key, value)
        print("\n=====    END   =====")
        while True:
            mode_input = input("---->").strip()
            if mode_input in dict.keys():
                mode_c = dict[mode_input]
                break
            else:
                print('Input error.You should be input a number')
        date_c = input("Please enter rank date: ").strip()
        pic_num_c = int(input(
            "Please enter rank number you want to download\n----> ").strip())
        return mode_c, date_c, pic_num_c

    while True:
        print("=====   MODE   =====\n")
        for key, value in rank_mode_dict.items():
            print(f"    {key} : {value[0]}")
        print("\n=====    END   =====")
        choice = str(input('Please choose mode , or enter 0 to quit\n---->').strip())
        if not choice.isdigit():
            print('Please enter number')
            continue
        if choice == '0':
            break
        elif choice == '1':
            content = 'illust'
            mode, date, pic_num = check_dict(rank_mode_dict[choice][1])
            id_list = pixiv_interface.get_rank_id_list(date, pic_num, mode, content)
            pixiv_interface.all_download(id_list)
        elif choice == '2':
            mode, date, pic_num = check_dict(rank_mode_dict[choice][1])
            id_list = pixiv_interface.get_rank_id_list(date, pic_num, mode)
            pixiv_interface.all_download(id_list)
        else:
            print('Enter error ,Please try again')


def liked_artist_mode():
    artist_id = input('Please enter your favorite artist number \n----> ').strip()
    id_list = pixiv_interface.liked_user_illustlist(artist_id)
    print("Will be download all illust of this artist")
    pixiv_interface.all_download(id_list)


func_dic = {
    '1': ['Rank mode', rank_mode],
    '2': ['Artist mode', liked_artist_mode],
}

def run():
    global func_dic
    while True:
        print("=====   MODE   =====\n")
        for key, value in func_dic.items():
            print(f"    {key} : {value[0]}")
        print("\n=====    END   =====")
        choice = input('Please enter a number, or enter 0 to quit').strip()
        if choice=='0':
            break
        func_dic[choice][1]()