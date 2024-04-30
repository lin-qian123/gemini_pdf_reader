# 基于google-gemini的pdf阅读问答

## 安装
使用linux终端或者Windows中git bash执行  
```python
git clone https://github.com/lin-qian123/gemini_pdf_reader.git
```
安装python依赖库  
```pyhton
pip install requirements.txt
```

## 使用
更改环境变量文件.env中的API为自己的API.  
新建文件夹名为pdf，在此文件夹下放入需要阅读的pdf文件.  
运行load.py文件，运行成功后可以看到vec_data文件夹下多出与pdf文件名称相同的.npy与.pkl文件.  
之后将ask.py文件中path改为相应的pdf文件，问题改为需要问的问题即可运行.  
