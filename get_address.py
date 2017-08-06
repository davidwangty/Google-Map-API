import requests
import json
import time

# 這是Google Maps Geocoding API Web 使用所需要的金鑰
# https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=zh-tw 可授權取得金鑰
key = []
with open("金鑰.txt") as keys:
	for k in keys:
		key.append(k[:-1])

key_num = 0

timenow = time.strftime("%H_%M_%S")

# 引入座標檔案
with open("座標.txt") as map_code:
	# 輸出地址的檔案
	with open("地址_" + timenow + ".txt", "w", encoding="UTF-8") as addresses:
		for x in map_code:
			try:
				# 發送請求至該網址並取得結果，若有金鑰已達上限，會換下一個
				check = 1
				while check:
					results = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}&language=zh-TW".format(x.replace("	", ",")[:-1], key[key_num])).text
					res_dict = json.loads(results)
					if res_dict["status"] == "OK":
						break
					elif res_dict["status"] == "OVER_QUERY_LIMIT":
						key_num += 1

				# 將地址前面多餘的字去掉
				address = res_dict["results"][0]["formatted_address"]
				if address.find("中和區") >= 0:
					address = address[address.find("中和區") + 3:]
				else:
					address = address[address.find("新北市") + 3:]
				print(x[:-1], address)
				addresses.write(address.strip() + "\n")
			except Exception as e:
				address.write(e)
				# 若OK 表示請求成功，若是OVER_QUERY_LIMIT表示金鑰每日請球次數已達上限(一天2500次)
				if res_dict["status"] == "OVER_QUERY_LIMIT":
					print("金鑰每日請求次數皆已達上限(1天2500次)")
					break
				else:
					print("請求結果:", res_dict["status"])


				print(e)
				print("目前請求座標: {0} 發生錯誤，若要繼續請輸入 go ".format(x.replace("	", ",")[:-1]))
				ans = input()
				if ans == "go":
					addresses.write("\n")
				else:
					break
		print("結果儲存在: " + "地址_" + timenow + ".txt")

			

