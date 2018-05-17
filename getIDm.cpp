#include <stdio.h>
#include <string>
#include <string.h>
#include "RCS620S.h"

int main()
{
    RCS620S rcs620s;

    //初期化
    int ret = rcs620s.initDevice();
    if (!ret)
    {
        printf("can't open pasori\n");
        return 0;
    }
    
    //読み取り部分
    char s[256] = {'\0'};
    do
    {
        //ここで読み取る
        ret = rcs620s.polling();

        if (ret)
        {
            //idを取得
            uint8_t *idm = rcs620s.idm;
            //変数sに出力
            sprintf(s, "%02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x\n",
                    idm[0], idm[1], idm[2], idm[3],
                    idm[4], idm[5], idm[6], idm[7]);
        }
        
    } //出力がなければ、繰り返し
    while (strlen(s) == 0);
    
    //出力
    printf(s);

    //読み取りをオフにする
    rcs620s.rfOff();

    return 0;
}
