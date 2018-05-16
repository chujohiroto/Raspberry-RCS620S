#include <inttypes.h>
#include <wiringSerial.h>

class HardwareSerial
{
private:
    int serialFd;

    public:
    HardwareSerial();
    ~HardwareSerial();

    void write(const uint8_t* data, uint16_t len);
    uint8_t read();
    bool available();
    void flush();
};

extern HardwareSerial Serial;
