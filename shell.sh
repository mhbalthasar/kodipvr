#!/bin/bash
mkdir src
git clone https://github.com.cnpmjs.org/aowatchsea/Aran
cp ./Aran/all.m3u ./src/src1.m3u8
git clone https://github.com.cnpmjs.org/SPX372928/MyIPTV
cp ./MyIPTV/上海百视通联通ip版.txt ./src/百事通联通.txt
cp ./MyIPTV/北方广电辽宁有线CDN版.txt ./src/辽宁有线.txt

cat ./src/src1.m3u8 > ./result.m3u8
echo -e "\r\n" >> ./result.m3u8
cat ./src/custom.m3u8 >> ./result.m3u8
rm -rf ./Aran
rm -rf ./MyIPTV
