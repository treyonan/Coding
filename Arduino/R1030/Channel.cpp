#include "Channel.h"

Channel::Channel()
  : IBusBM() {
}
void Channel::ReadChannels() {
  Channel::loop();
  for (int i = 0; i < 9; i++) {
    Reading[i] = Channel::readChannel(i);
  }
}
void Channel::Init(int channelNum, float _RawMin, float _RawMax, float _ScaledMin, float _ScaledMax, float _CutOff) {
  RawMin[channelNum] = _RawMin;
  RawMax[channelNum] = _RawMax;
  ScaledMin[channelNum] = _ScaledMin;
  ScaledMax[channelNum] = _ScaledMax;
  CutOff[channelNum] = _CutOff;
}
float Channel::Map(int channelNum) {
  Output[channelNum] = constrain(map(Reading[channelNum], RawMin[channelNum], RawMax[channelNum], ScaledMin[channelNum], ScaledMax[channelNum]), 1000, 2000);
  if (Output[channelNum] > (CutOff[channelNum] - 10) && Output[channelNum] < (CutOff[channelNum] + 30)) {
    Output[channelNum] = CutOff[channelNum];
  }
  return Output[channelNum];
}
