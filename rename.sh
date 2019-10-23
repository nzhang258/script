#将文件夹中的名字从0~8改为10_test~18_test

for((i=0;i<9;++i));
do
a=9;
b=$[$i+$a];
echo $b"_test";
#mv $i $b"_test";
done
