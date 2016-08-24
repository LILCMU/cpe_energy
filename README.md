# A/C Energy Consumption Measurement System 
# Department of Computer Engineering, 
# Faculty of Engineering, Chiang Mai University, Thailand

/python - 	contains the script that communicates with the power meter modules via ModBus
 			It usually runs on a Raspberry Pi. 

The sysetem can be accessed from the following link [https://lilcmu.github.io/cpe_energy](https://lilcmu.github.io/cpe_energy)

Configuration:  ***Need to change value on line with comment***
js/config.json
```
          {
            "server": {  
              "name": "Floor#4",      // name your map    
              "url": "https://data.learninginventions.org/channels/"   // your URL Server    
            },
            "room": [
              {
                "name": "401",    // your room name
                "list": [
                  {
                    "no": 30,             // your label order 
                    "channels": 131      // your channels ID from your server 
                  },
                  {
                    "no": 31,
                    "channels": 132
                  },
                  {
                    "no": 28,
                    "channels": 129
                  }
                ],
                "sum_unit_used": 0
              },
              {
                "name": "402",
                "list": [
                  {
                    "no": 1,
                    "channels": 102
                  },
                  {
                    "no": 3,
                    "channels": 104
                  },
                  {
                    "no": 5,
                    "channels": 106
                  }
                ],
                "sum_unit_used": 0
              }
            ]
          }
```
