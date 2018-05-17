#include <stdio.h>
#include <string>
#include <string.h>
#include "RCS620S.h"
#include "unistd.h"
#include <stdlib.h>

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
    char *s;
    char *p;
    
    
    s = (char*)calloc(256,sizeof(char));
    p = (char*)calloc(256,sizeof(char));
    

    if (s==NULL || p ==NULL) {
        return 0;
    }
    
    while (true){
        //ここで読み取る
        ret = rcs620s.polling();
        if (ret)
        {
            uint8_t *pmm = rcs620s.pmm;
            //idを取得
            uint8_t *idm = rcs620s.idm;
            //変数sに出力
            sprintf(p, "PMm:  %02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x\n",
                    pmm[0], pmm[1], pmm[2], pmm[3],
                    pmm[4], pmm[5], pmm[6], pmm[7]);
            sprintf(s, "IDm:  %02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x\n",
                    idm[0], idm[1], idm[2], idm[3],
                    idm[4], idm[5], idm[6], idm[7]);
        }
        if (strlen(s) != 0) {
            //出力
            printf(p);
            printf(s);
            free(s);
            free(p);
            
            s = (char*)calloc(256,sizeof(char));
            p = (char*)calloc(256,sizeof(char));
            
            sleep(3);
        }
    }

    //読み取りをオフにする
    rcs620s.rfOff();
    
    free(s);
    free(p);

    return 0;
}

