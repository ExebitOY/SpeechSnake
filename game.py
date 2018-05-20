
# DON'T BE A DICK PUBLIC LICENSE
#
#> Version 1.1, December 2016
#
#> Copyright (C) 2018 Jaakko Sirén & Olli Peura
#
#Everyone is permitted to copy and distribute verbatim or modified
#copies of this license document.
#
#> DON'T BE A DICK PUBLIC LICENSE
#> TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#1. Do whatever you like with the original work, just don't be a dick.
#
#   Being a dick includes - but is not limited to - the following instances:
#
# 1a. Outright copyright infringement - Don't just copy this and change the name.
# 1b. Selling the unmodified original with no work done what-so-ever, that's REALLY being a dick.
# 1c. Modifying the original work to contain hidden harmful content. That would make you a PROPER dick.
#
#2. If you become rich through modifications, related works/services, or supporting the original work,
#share the love. Only a dick would make loads off this work and not buy the original work's
#creator(s) a pint.
#
#3. Code is provided with no warranty. Using somebody else's code and bitching when it goes wrong makes
#you a DONKEY dick. Fix the problem yourself. A non-dick would submit the fix back.




#####        LICENCE OF SPEECH_RECOGNITION LIBRARY: https://github.com/Uberi/speech_recognition     ######


#Copyright (c) 2014-2017, Anthony Zhang <azhang9@gmail.com>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions #are met:
#
#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in #the documentation and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from #this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.







import random
import speech_recognition as sr
import google.cloud.storage
import socket

def getSpeech():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.operation_timeout = 3.0
    r.pause_threshold = 0.5
    with sr.Microphone(device_index = None, sample_rate = 48000, chunk_size = 1024) as source:
        print("Say something!")
        audio = r.listen(source)
     
    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_bing(audio)`
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        
        return "banana"
    except sr.RequestError as e:
        print("Could not request results from some speech Recognition service; {0}".format(e))
        return "banana"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/socketname")
while True:
    a = getSpeech()
    s.send(str.encode(a))
