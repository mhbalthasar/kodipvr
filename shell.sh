#!/bin/bash
mkdir src
mkdir src/txt
git clone https://github.com.cnpmjs.org/aowatchsea/Aran
cp ./Aran/all.m3u ./src/src1.m3u8
git clone https://github.com.cnpmjs.org/SPX372928/MyIPTV
cp ./MyIPTV/*.txt ./src/txt/
rm ./src/txt/Y失效*.txt

cat ./src/src1.m3u8 > ./result.m3u8
echo -e "\r\n" >> ./result.m3u8
cat ./src/custom.m3u8 >> ./result.m3u8
rm -rf ./Aran
rm -rf ./MyIPTV
