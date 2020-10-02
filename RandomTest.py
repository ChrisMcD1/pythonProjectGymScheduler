# from datetime import datetime
# import timeit
#
# now = datetime.now()
# currentTime = now.strftime("%H:%M:%S")
#
# splitCurrentTime = []
# for temp in currentTime.split(':'):
#     splitCurrentTime.append(int(temp))
# setupTime = """
# from datetime import datetime
# now = datetime.now()
# currentTime = now.strftime("%H:%M:%S")
# """
#
# slow = """
# splitCurrentTime = []
# for temp in currentTime.split(':'):
#     splitCurrentTime.append(int(temp))
# """
#
# fast = "fastSplitCurrent = [int(temp) for temp in currentTime.split(':')]"
#
# print(timeit.timeit(stmt=slow, setup=setupTime, number=10000000))
# print(timeit.timeit(stmt=fast, setup=setupTime, number=10000000))
#
# fastSplitCurrent = [int(temp) for temp in currentTime.split(':')]
# # print(fastSplitCurrent)
# # print(splitCurrentTime == fastSplitCurrent)


with open("GTCredentials.txt", "r") as f:
    combinedUserPassword = f.read().splitlines()
    username = combinedUserPassword[0]
    password = combinedUserPassword[1]
    print(repr(username))
    print(repr(password))
