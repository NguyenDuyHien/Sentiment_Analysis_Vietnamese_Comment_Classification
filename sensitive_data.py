# encoding=utf8
import sys
import re
from pyvi import ViTokenizer
import csv

reload(sys)
sys.setdefaultencoding('utf8')

fh=open("Training_demo.csv","r")

# Comment và nhãn cách nhau bởi dấu +
reader = csv.reader(fh, delimiter='+')

# Chứa số lần xuất hiện của từ tương ứng với các nhãn. Vd: {nhãn 1 : {từ : số lần xuất hiện trong nhãn 1}}
dataset={}

# Chứa số lượng câu của từng nhãn
no_of_items={}

# Chứa số lần xuất hiện của từ ứng với từng nhãn. Vd: {từ : {nhã 1 : số lần xuất hiện trong nhãn 1}}
feature_set={}

# Xử lý từng comment
for row in reader:
	# Khởi tạo giá trị mặc định cho biến no_of_items
	no_of_items.setdefault(row[1],0)
	# Tăng số lượng câu ứng với từng nhãn lên 1
	no_of_items[row[1]]+=1
	# Khởi tạo giá trị mặc định cho biến dataset
	dataset.setdefault(row[1],{})
	# Tách từ và lưu vào file split_data
	split_data = re.split('[\s,.;:?!-]', ViTokenizer.tokenize(row[0].decode('utf-8')))
	# Xử lý từng từ trong file split_data
	for i in split_data:
		# Loại bỏ ký tự '' xuất hiện khi tách từ
		if i != "":
			# Khởi tạo bộ đếm từ cho dataset (nếu chưa được khởi tạo)
			dataset[row[1]].setdefault(i.lower(),0)
			# Tăng số lần xuất hiện với nhãn tương ứng trong biến dataset
			dataset[row[1]][i.lower()]+=1
			# Khởi tạo bộ đếm cho từ mới trong feature set (nếu chưa được khởi tạo)
			feature_set.setdefault(i.lower(),{})
			# Khởi tạo biến đếm cho nhãn (nếu chưa được khởi tạo)
			feature_set[i.lower()].setdefault(row[1],0)
			# Tăng biến đếm cho nhãn tương ứng
			feature_set[i.lower()][row[1]]+=1