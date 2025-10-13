docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

warmup
low_load: {
    executor: 'constant-vus', 
    vus: 10,
    duration: '30s',
},
```bash

         /\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 

     execution: local
        script: load.js
        output: -

     scenarios: (100.00%) 1 scenario, 10 max VUs, 1m0s max duration (incl. graceful stop):
              * low_load: 10 looping VUs for 30s (gracefulStop: 30s)



  █ THRESHOLDS 

    errors
    ✓ 'rate<0.05' rate=0.00%

    http_req_duration
    ✓ 'p(95)<500' p(95)=5.9ms


  █ TOTAL RESULTS 

    checks_total.......: 20064   668.583825/s
    checks_succeeded...: 100.00% 20064 out of 20064
    checks_failed......: 0.00%   0 out of 20064

    ✓ status 200

    CUSTOM
    errors.........................: 0.00%  0 out of 20064

    HTTP
    http_req_duration..............: avg=4.13ms  min=891µs   med=4.07ms  max=29.83ms p(90)=5.49ms  p(95)=5.9ms  
      { expected_response:true }...: avg=4.13ms  min=891µs   med=4.07ms  max=29.83ms p(90)=5.49ms  p(95)=5.9ms  
    http_req_failed................: 0.00%  0 out of 20064
    http_reqs......................: 20064  668.583825/s

    EXECUTION
    iteration_duration.............: avg=14.93ms min=11.07ms med=14.87ms max=42.62ms p(90)=16.38ms p(95)=16.84ms
    iterations.....................: 20064  668.583825/s
    vus............................: 10     min=10         max=10
    vus_max........................: 10     min=10         max=10

    NETWORK
    data_received..................: 2.9 MB 98 kB/s
    data_sent......................: 1.7 MB 56 kB/s




running (0m30.0s), 00/10 VUs, 20064 complete and 0 interrupted iterations
low_load ✓ [======================================] 10 VUs  30s
---
d.rizun@aiokiddy load_tests % ./monitoring.sh
NAME      CPU %     MEM USAGE / LIMIT    NET I/O
go-v      0.00%     7.355MiB / 7.654GiB   74kB / 95.8kB
go-v      0.35%     8.062MiB / 7.654GiB   74.4kB / 96.3kB
go-v      16.19%    8.891MiB / 7.654GiB   1.37MB / 1.22MB
go-v      15.03%    8.797MiB / 7.654GiB   2.57MB / 2.26MB
go-v      14.45%    8.855MiB / 7.654GiB   3.76MB / 3.29MB
go-v      16.35%    8.949MiB / 7.654GiB   4.93MB / 4.31MB
go-v      15.92%    9.508MiB / 7.654GiB   6.11MB / 5.33MB
go-v      14.95%    9.004MiB / 7.654GiB   7.43MB / 6.48MB
go-v      14.70%    10.71MiB / 7.654GiB   8.63MB / 7.52MB
go-v      16.24%    10.67MiB / 7.654GiB   9.83MB / 8.56MB
go-v      0.00%     10.77MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.77MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.23%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.53MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.01%     10.79MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.54MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.53MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.53MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.25%     10.53MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.53MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.01%     10.79MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.54MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.22%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.52MiB / 7.654GiB   10.1MB / 8.77MB
go-v      0.00%     10.53MiB / 7.654GiB   10.1MB / 8.78MB
go-v      0.00%     10.53MiB / 7.654GiB   10.1MB / 8.78MB
go-v      0.12%     11.29MiB / 7.654GiB   10.1MB / 8.78MB
go-v      0.00%     10.78MiB / 7.654GiB   10.1MB / 8.78MB
go-v      0.00%     10.54MiB / 7.654GiB   10.1MB / 8.78MB
```


medium_load: {
    executor: 'constant-vus',
    vus: 50,
    duration: '1m',
}
```bash
d.rizun@aiokiddy load_tests % k6 run load.js

         /\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 

     execution: local
        script: load.js
        output: -

     scenarios: (100.00%) 1 scenario, 50 max VUs, 1m30s max duration (incl. graceful stop):
              * medium_load: 50 looping VUs for 1m0s (gracefulStop: 30s)



  █ THRESHOLDS 

    errors
    ✓ 'rate<0.05' rate=0.00%

    http_req_duration
    ✓ 'p(95)<500' p(95)=12.25ms


  █ TOTAL RESULTS 

    checks_total.......: 208677  3480.132797/s
    checks_succeeded...: 100.00% 208677 out of 208677
    checks_failed......: 0.00%   0 out of 208677

    ✓ status 200

    CUSTOM
    errors.........................: 0.00%  0 out of 208677

    HTTP
    http_req_duration..............: avg=4.19ms  min=21µs    med=2.77ms  max=143.3ms  p(90)=7.95ms p(95)=12.25ms
      { expected_response:true }...: avg=4.19ms  min=21µs    med=2.77ms  max=143.3ms  p(90)=7.95ms p(95)=12.25ms
    http_req_failed................: 0.00%  0 out of 208677
    http_reqs......................: 208677 3480.132797/s

    EXECUTION
    iteration_duration.............: avg=14.36ms min=10.53ms med=12.92ms max=153.41ms p(90)=18.2ms p(95)=22.47ms
    iterations.....................: 208677 3480.132797/s
    vus............................: 50     min=50          max=50
    vus_max........................: 50     min=50          max=50

    NETWORK
    data_received..................: 31 MB  512 kB/s
    data_sent......................: 17 MB  289 kB/s




running (1m00.0s), 00/50 VUs, 208677 complete and 0 interrupted iterations
---
NAME      CPU %     MEM USAGE / LIMIT     NET I/O
go-v      0.02%     11.05MiB / 7.654GiB   10.1MB / 8.79MB
go-v      62.92%    14.9MiB / 7.654GiB   13MB / 11.3MB
go-v      51.33%    15.73MiB / 7.654GiB   20.3MB / 17.7MB
go-v      61.09%    15.75MiB / 7.654GiB   27.2MB / 23.6MB
go-v      52.72%    15.93MiB / 7.654GiB   33.7MB / 29.3MB
go-v      62.01%    17.88MiB / 7.654GiB   40.4MB / 35.1MB
go-v      62.71%    17.98MiB / 7.654GiB   47MB / 40.8MB
go-v      58.24%    17.77MiB / 7.654GiB   53.4MB / 46.4MB
go-v      45.65%    17.58MiB / 7.654GiB   59.4MB / 51.6MB
go-v      64.26%    17.7MiB / 7.654GiB   66MB / 57.3MB
go-v      62.34%    17.69MiB / 7.654GiB   73.2MB / 63.6MB
go-v      56.86%    18.23MiB / 7.654GiB   80MB / 69.4MB
go-v      62.38%    18.21MiB / 7.654GiB   86.7MB / 75.3MB
go-v      46.46%    18.02MiB / 7.654GiB   93.1MB / 80.9MB
go-v      34.55%    17.97MiB / 7.654GiB   98.6MB / 85.6MB
go-v      36.66%    18.29MiB / 7.654GiB   104MB / 90.5MB
go-v      36.82%    18.07MiB / 7.654GiB   110MB / 95.3MB
go-v      38.33%    18.09MiB / 7.654GiB   114MB / 99.4MB
go-v      0.00%     16.98MiB / 7.654GiB   114MB / 99.4MB
go-v      0.20%     17.96MiB / 7.654GiB   114MB / 99.4MB
go-v      0.00%     16.97MiB / 7.654GiB   114MB / 99.4MB
go-v      0.00%     16.96MiB / 7.654GiB   114MB / 99.4MB
go-v      0.02%     17MiB / 7.654GiB    114MB / 99.4MB
go-v      0.00%     17MiB / 7.654GiB    114MB / 99.4MB
go-v      0.00%     17MiB / 7.654GiB    114MB / 99.4MB
```



high_load: {
    executor: 'constant-vus',
    vus: 100,
    duration: '1m',
},
```bash

         /\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 

     execution: local
        script: load.js
        output: -

     scenarios: (100.00%) 1 scenario, 100 max VUs, 1m30s max duration (incl. graceful stop):
              * high_load: 100 looping VUs for 1m0s (gracefulStop: 30s)



  █ THRESHOLDS 

    errors
    ✓ 'rate<0.05' rate=0.00%

    http_req_duration
    ✓ 'p(95)<500' p(95)=20.07ms


  █ TOTAL RESULTS 

    checks_total.......: 331058  5514.808281/s
    checks_succeeded...: 100.00% 331058 out of 331058
    checks_failed......: 0.00%   0 out of 331058

    ✓ status 200

    CUSTOM
    errors.........................: 0.00%  0 out of 331058

    HTTP
    http_req_duration..............: avg=7.94ms  min=487µs  med=5.89ms  max=134.04ms p(90)=15.62ms p(95)=20.07ms
      { expected_response:true }...: avg=7.94ms  min=487µs  med=5.89ms  max=134.04ms p(90)=15.62ms p(95)=20.07ms
    http_req_failed................: 0.00%  0 out of 331058
    http_reqs......................: 331058 5514.808281/s

    EXECUTION
    iteration_duration.............: avg=18.12ms min=10.6ms med=16.05ms max=144.16ms p(90)=25.79ms p(95)=30.28ms
    iterations.....................: 331058 5514.808281/s
    vus............................: 100    min=100         max=100
    vus_max........................: 100    min=100         max=100

    NETWORK
    data_received..................: 49 MB  811 kB/s
    data_sent......................: 28 MB  458 kB/s




running (1m00.0s), 000/100 VUs, 331058 complete and 0 interrupted iterations
---
d.rizun@aiokiddy load_tests % ./monitoring.sh
NAME      CPU %     MEM USAGE / LIMIT     NET I/O
go-v      0.27%     12.82MiB / 7.654GiB   114MB / 99.4MB
go-v      94.26%    17.5MiB / 7.654GiB   118MB / 103MB
go-v      98.48%    18.18MiB / 7.654GiB   129MB / 112MB
go-v      69.07%    18.49MiB / 7.654GiB   139MB / 121MB
go-v      66.82%    18.38MiB / 7.654GiB   150MB / 130MB
go-v      102.85%   18.26MiB / 7.654GiB   161MB / 140MB
go-v      84.63%    18.58MiB / 7.654GiB   172MB / 150MB
go-v      101.09%   18.77MiB / 7.654GiB   183MB / 159MB
go-v      76.67%    18.65MiB / 7.654GiB   193MB / 168MB
go-v      101.84%   19.06MiB / 7.654GiB   204MB / 177MB
go-v      101.25%   18.9MiB / 7.654GiB   215MB / 187MB
go-v      56.15%    19.77MiB / 7.654GiB   224MB / 194MB
go-v      64.32%    18.72MiB / 7.654GiB   233MB / 202MB
go-v      58.50%    18.64MiB / 7.654GiB   241MB / 210MB
go-v      65.62%    19.04MiB / 7.654GiB   250MB / 217MB
go-v      66.73%    19.07MiB / 7.654GiB   259MB / 225MB
go-v      59.28%    19.57MiB / 7.654GiB   269MB / 234MB
go-v      51.02%    19.33MiB / 7.654GiB   278MB / 241MB
go-v      0.23%     17.83MiB / 7.654GiB   279MB / 242MB
go-v      0.00%     17.8MiB / 7.654GiB   279MB / 242MB
go-v      0.00%     17.81MiB / 7.654GiB   279MB / 242MB
go-v      0.00%     17.8MiB / 7.654GiB   279MB / 242MB
go-v      0.24%     19.03MiB / 7.654GiB   279MB / 242MB
go-v      0.00%     18.05MiB / 7.654GiB   279MB / 242MB
go-v      0.00%     17.8MiB / 7.654GiB   279MB / 242MB
go-v      0.00%     17.81MiB / 7.654GiB   279MB / 242MB
go-v      0.00%     17.8MiB / 7.654GiB   279MB / 242MB
go-v      0.00%     17.8MiB / 7.654GiB   279MB / 242MB
^C^C^C
d.rizun@aiokiddy load_tests % 

```



stress_test: {
    executor: 'constant-vus',
    vus: 500,
    duration: '1m',
},

```bash

         /\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 

     execution: local
        script: load.js
        output: -

     scenarios: (100.00%) 1 scenario, 500 max VUs, 1m30s max duration (incl. graceful stop):
              * stress_test: 500 looping VUs for 1m0s (gracefulStop: 30s)



  █ THRESHOLDS 

    errors
    ✓ 'rate<0.05' rate=0.00%

    http_req_duration
    ✓ 'p(95)<500' p(95)=99.72ms


  █ TOTAL RESULTS 

    checks_total.......: 468090  7795.268592/s
    checks_succeeded...: 100.00% 468090 out of 468090
    checks_failed......: 0.00%   0 out of 468090

    ✓ status 200

    CUSTOM
    errors.........................: 0.00%  0 out of 468090

    HTTP
    http_req_duration..............: avg=53.74ms min=2.42ms  med=47.7ms  max=556.22ms p(90)=85.07ms p(95)=99.72ms 
      { expected_response:true }...: avg=53.74ms min=2.42ms  med=47.7ms  max=556.22ms p(90)=85.07ms p(95)=99.72ms 
    http_req_failed................: 0.00%  0 out of 468090
    http_reqs......................: 468090 7795.268592/s

    EXECUTION
    iteration_duration.............: avg=64.1ms  min=12.56ms med=58.06ms max=566.27ms p(90)=95.26ms p(95)=110.02ms
    iterations.....................: 468090 7795.268592/s
    vus............................: 500    min=500         max=500
    vus_max........................: 500    min=500         max=500

    NETWORK
    data_received..................: 69 MB  1.1 MB/s
    data_sent......................: 39 MB  647 kB/s




running (1m00.0s), 000/500 VUs, 468090 complete and 0 interrupted iterations
---
NAME      CPU %     MEM USAGE / LIMIT     NET I/O
go-v      0.59%     14.65MiB / 7.654GiB   279MB / 242MB
go-v      99.14%    30.27MiB / 7.654GiB   289MB / 251MB
go-v      109.17%   32.88MiB / 7.654GiB   308MB / 267MB
go-v      118.44%   32.58MiB / 7.654GiB   325MB / 282MB
go-v      117.80%   33.16MiB / 7.654GiB   342MB / 296MB
go-v      96.13%    32.88MiB / 7.654GiB   361MB / 313MB
go-v      241.40%   32.92MiB / 7.654GiB   376MB / 326MB
go-v      76.89%    29.99MiB / 7.654GiB   390MB / 338MB
go-v      73.56%    29.87MiB / 7.654GiB   404MB / 352MB
go-v      52.83%    29.76MiB / 7.654GiB   415MB / 363MB
go-v      77.87%    30.5MiB / 7.654GiB   429MB / 377MB
go-v      63.33%    30MiB / 7.654GiB    442MB / 389MB
go-v      71.27%    30.61MiB / 7.654GiB   455MB / 402MB
go-v      70.99%    30.48MiB / 7.654GiB   469MB / 415MB
go-v      82.49%    30.42MiB / 7.654GiB   481MB / 428MB
go-v      63.92%    29.98MiB / 7.654GiB   493MB / 439MB
go-v      89.45%    31.24MiB / 7.654GiB   506MB / 452MB
go-v      0.00%     27.42MiB / 7.654GiB   515MB / 460MB
```



high_stress_test: {
    executor: 'constant-vus',
    vus: 1000,
    duration: '1m',
}

```bash
         /\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 

     execution: local
        script: load.js
        output: -

     scenarios: (100.00%) 1 scenario, 1000 max VUs, 1m30s max duration (incl. graceful stop):
              * high_stress_test: 1000 looping VUs for 1m0s (gracefulStop: 30s)



  █ THRESHOLDS 

    errors
    ✓ 'rate<0.05' rate=0.00%

    http_req_duration
    ✓ 'p(95)<500' p(95)=243.88ms


  █ TOTAL RESULTS 

    checks_total.......: 450444  7493.863834/s
    checks_succeeded...: 100.00% 450444 out of 450444
    checks_failed......: 0.00%   0 out of 450444

    ✓ status 200

    CUSTOM
    errors.........................: 0.00%  0 out of 450444

    HTTP
    http_req_duration..............: avg=122.22ms min=1.75ms  med=106.59ms max=593.95ms p(90)=205.76ms p(95)=243.88ms
      { expected_response:true }...: avg=122.22ms min=1.75ms  med=106.59ms max=593.95ms p(90)=205.76ms p(95)=243.88ms
    http_req_failed................: 0.00%  0 out of 450444
    http_reqs......................: 450444 7493.863834/s

    EXECUTION
    iteration_duration.............: avg=133.29ms min=13.66ms med=117.14ms max=657.65ms p(90)=216.65ms p(95)=256.17ms
    iterations.....................: 450444 7493.863834/s
    vus............................: 1000   min=1000        max=1000
    vus_max........................: 1000   min=1000        max=1000

    NETWORK
    data_received..................: 66 MB  1.1 MB/s
    data_sent......................: 37 MB  622 kB/s




running (1m00.1s), 0000/1000 VUs, 450444 complete and 0 interrupted iterations
high_stress_test ✓ [======================================] 1000 VUs  1m0s
---
NAME      CPU %     MEM USAGE / LIMIT     NET I/O
go-v      0.71%     26.88MiB / 7.654GiB   515MB / 460MB
go-v      147.27%   49.16MiB / 7.654GiB   523MB / 468MB
go-v      117.52%   51.02MiB / 7.654GiB   540MB / 483MB
go-v      194.22%   56.99MiB / 7.654GiB   558MB / 500MB
go-v      129.45%   54.05MiB / 7.654GiB   575MB / 514MB
go-v      216.45%   54.82MiB / 7.654GiB   593MB / 531MB
go-v      147.26%   53.31MiB / 7.654GiB   610MB / 546MB
go-v      78.20%    47.77MiB / 7.654GiB   631MB / 564MB
go-v      146.26%   50.52MiB / 7.654GiB   649MB / 581MB
go-v      177.19%   46.63MiB / 7.654GiB   664MB / 594MB
go-v      112.57%   47.66MiB / 7.654GiB   681MB / 609MB
go-v      164.87%   48.92MiB / 7.654GiB   697MB / 623MB
go-v      49.12%    46.9MiB / 7.654GiB   709MB / 634MB
go-v      112.89%   47.74MiB / 7.654GiB   722MB / 647MB
go-v      85.29%    47.05MiB / 7.654GiB   736MB / 660MB
go-v      55.84%    48.53MiB / 7.654GiB   747MB / 672MB
go-v      25.76%    42.5MiB / 7.654GiB   759MB / 683MB
^C^C

```