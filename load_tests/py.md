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



   THRESHOLDS 

    errors
    ✓ 'rate<0.05' rate=0.00%

    http_req_duration
    ✓ 'p(95)<500' p(95)=8.49ms


  TOTAL RESULTS 

    checks_total.......: 5204    86.729913/s
    checks_succeeded...: 100.00% 5204 out of 5204
    checks_failed......: 0.00%   0 out of 5204

    ✓ status 200

    CUSTOM
    errors.........................: 0.00%  0 out of 5204

    HTTP
    http_req_duration..............: avg=22.59ms min=1.77ms  med=4.97ms  max=4.97s p(90)=6.6ms   p(95)=8.49ms 
      { expected_response:true }...: avg=22.59ms min=1.77ms  med=4.97ms  max=4.97s p(90)=6.6ms   p(95)=8.49ms 
    http_req_failed................: 0.00%  0 out of 5204
    http_reqs......................: 5204   86.729913/s

    EXECUTION
    iteration_duration.............: avg=32.98ms min=11.93ms med=15.39ms max=4.98s p(90)=16.94ms p(95)=18.79ms
    iterations.....................: 5204   86.729913/s
    vus............................: 8      min=8         max=10
    vus_max........................: 10     min=10        max=10

    NETWORK
    data_received..................: 765 kB 13 kB/s
    data_sent......................: 436 kB 7.3 kB/s




running (1m00.0s), 00/10 VUs, 5204 complete and 8 interrupted iterations
---
NAME      CPU %     MEM USAGE / LIMIT     NET I/O
py-v      34.53%    94.38MiB / 7.654GiB   11.3MB / 16.1MB
py-v      40.34%    99.68MiB / 7.654GiB   13MB / 18.7MB
py-v      19.04%    95.36MiB / 7.654GiB   14.3MB / 20.3MB
py-v      7.40%     86.76MiB / 7.654GiB   14.6MB / 20.5MB
py-v      0.33%     86.37MiB / 7.654GiB   14.6MB / 20.6MB
py-v      3.55%     86.59MiB / 7.654GiB   14.6MB / 20.6MB
py-v      0.34%     86.3MiB / 7.654GiB   14.6MB / 20.6MB
py-v      0.28%     86.32MiB / 7.654GiB   14.7MB / 20.6MB
py-v      0.35%     86.26MiB / 7.654GiB   14.7MB / 20.6MB
py-v      0.57%     86.25MiB / 7.654GiB   14.7MB / 20.6MB
py-v      0.29%     86.24MiB / 7.654GiB   14.7MB / 20.6MB
py-v      0.31%     86.24MiB / 7.654GiB   14.7MB / 20.6MB
py-v      0.35%     86.24MiB / 7.654GiB   14.7MB / 20.6MB
py-v      0.35%     86.24MiB / 7.654GiB   14.7MB / 20.6MB
py-v      0.28%     86.81MiB / 7.654GiB   14.7MB / 20.6MB
```


medium_load: {
    executor: 'constant-vus',
    vus: 50,
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

     scenarios: (100.00%) 1 scenario, 50 max VUs, 1m30s max duration (incl. graceful stop):
              * medium_load: 50 looping VUs for 1m0s (gracefulStop: 30s)

  █ THRESHOLDS 

    errors
    ✓ 'rate<0.05' rate=0.41%

    http_req_duration
    ✓ 'p(95)<500' p(95)=33.82ms


  █ TOTAL RESULTS 

    checks_total.......: 10182  117.853008/s
    checks_succeeded...: 99.58% 10140 out of 10182
    checks_failed......: 0.41%  42 out of 10182

    ✗ status 200
      ↳  99% — ✓ 10140 / ✗ 42

    CUSTOM
    errors.........................: 0.41%  42 out of 10182

    HTTP
    http_req_duration..............: avg=336.95ms min=1.64ms  med=16.03ms max=1m0s   p(90)=25.24ms p(95)=33.82ms
      { expected_response:true }...: avg=89.82ms  min=1.64ms  med=16.01ms max=41.07s p(90)=24.99ms p(95)=33ms   
    http_req_failed................: 0.41%  42 out of 10182
    http_reqs......................: 10182  117.853008/s

    EXECUTION
    iteration_duration.............: avg=347.14ms min=11.78ms med=26.17ms max=1m0s   p(90)=35.41ms p(95)=44.83ms
    iterations.....................: 10182  117.853008/s
    vus............................: 1      min=1           max=50
    vus_max........................: 50     min=50          max=50

    NETWORK
    data_received..................: 1.5 MB 17 kB/s
    data_sent......................: 861 kB 10 kB/s
---
NAME      CPU %     MEM USAGE / LIMIT     NET I/O
py-v      118.81%   133.2MiB / 7.654GiB   21.2MB / 30.9MB
py-v      18.14%    108.2MiB / 7.654GiB   22.2MB / 31.5MB
py-v      0.31%     98.4MiB / 7.654GiB   22.6MB / 31.7MB
py-v      0.27%     98.75MiB / 7.654GiB   22.6MB / 31.8MB
py-v      3.43%     99.72MiB / 7.654GiB   22.6MB / 31.8MB
py-v      0.31%     98.61MiB / 7.654GiB   22.7MB / 31.9MB
py-v      0.40%     98.62MiB / 7.654GiB   22.7MB / 31.9MB
py-v      0.36%     98.91MiB / 7.654GiB   22.7MB / 32MB
py-v      3.50%     99.25MiB / 7.654GiB   22.7MB / 32MB
py-v      0.33%     98.77MiB / 7.654GiB   22.7MB / 32MB
py-v      0.29%     98.76MiB / 7.654GiB   22.7MB / 32MB
py-v      0.33%     98.79MiB / 7.654GiB   22.7MB / 32MB
py-v      2.05%     99.53MiB / 7.654GiB   22.7MB / 32.1MB
py-v      0.35%     98.79MiB / 7.654GiB   22.7MB / 32.1MB
py-v      0.34%     98.81MiB / 7.654GiB   22.8MB / 32.1MB
py-v      0.36%     99.3MiB / 7.654GiB   22.8MB / 32.1MB
py-v      0.92%     99.05MiB / 7.654GiB   22.8MB / 32.1MB
py-v      0.37%     98.87MiB / 7.654GiB   22.8MB / 32.1MB
py-v      0.32%     98.71MiB / 7.654GiB   22.8MB / 32.1MB
py-v      0.22%     97.51MiB / 7.654GiB   22.8MB / 32.1MB
py-v      0.40%     95.12MiB / 7.654GiB   22.8MB / 32.2MB
py-v      0.29%     94.84MiB / 7.654GiB   22.8MB / 32.2MB
py-v      0.35%     94.56MiB / 7.654GiB   22.8MB / 32.2MB
py-v      0.44%     94.55MiB / 7.654GiB   22.9MB / 32.2MB
py-v      0.32%     94.29MiB / 7.654GiB   22.9MB / 32.2MB
py-v      0.32%     94.44MiB / 7.654GiB   22.9MB / 32.2MB
py-v      0.24%     94.2MiB / 7.654GiB   22.9MB / 32.2MB
py-v      0.25%     94.2MiB / 7.654GiB   22.9MB / 32.2MB
py-v      0.28%     94.2MiB / 7.654GiB   22.9MB / 32.2MB
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
    ✓ 'rate<0.05' rate=0.72%

    http_req_duration
    ✓ 'p(95)<500' p(95)=68.5ms


  █ TOTAL RESULTS 

    checks_total.......: 13064  151.629333/s
    checks_succeeded...: 99.27% 12969 out of 13064
    checks_failed......: 0.72%  95 out of 13064

    ✗ status 200
      ↳  99% — ✓ 12969 / ✗ 95

    CUSTOM
    errors.........................: 0.72%  95 out of 13064

    HTTP
    http_req_duration..............: avg=534.66ms min=1.89ms med=38.54ms max=1m0s   p(90)=55.1ms  p(95)=68.5ms 
      { expected_response:true }...: avg=99.06ms  min=1.89ms med=38.47ms max=41.04s p(90)=54.35ms p(95)=64.26ms
    http_req_failed................: 0.72%  95 out of 13064
    http_reqs......................: 13064  151.629333/s

    EXECUTION
    iteration_duration.............: avg=544.87ms min=12.2ms med=48.73ms max=1m0s   p(90)=65.41ms p(95)=78.87ms
    iterations.....................: 13064  151.629333/s
    vus............................: 1      min=1           max=100
    vus_max........................: 100    min=100         max=100

    NETWORK
    data_received..................: 1.9 MB 22 kB/s
    data_sent......................: 1.1 MB 13 kB/s
---
NAME      CPU %     MEM USAGE / LIMIT     NET I/O
py-v      120.98%   116.1MiB / 7.654GiB   26.2MB / 37.7MB
py-v      127.55%   147.4MiB / 7.654GiB   30.9MB / 45.3MB
py-v      19.54%    117.1MiB / 7.654GiB   32.5MB / 46.6MB
py-v      0.36%     108.9MiB / 7.654GiB   32.9MB / 46.9MB
py-v      0.30%     109.1MiB / 7.654GiB   33MB / 47.1MB
py-v      0.50%     109.7MiB / 7.654GiB   33MB / 47.2MB
py-v      0.39%     109.1MiB / 7.654GiB   33MB / 47.2MB
py-v      0.33%     109.2MiB / 7.654GiB   33.1MB / 47.2MB
py-v      0.37%     109.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      1.90%     109.6MiB / 7.654GiB   33.1MB / 47.3MB
py-v      1.18%     110.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.39%     109.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.28%     109.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.30%     109.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.36%     109.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.36%     109.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.38%     109.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.34%     109.3MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.64%     109.5MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.34%     109.2MiB / 7.654GiB   33.1MB / 47.3MB
py-v      0.31%     108.5MiB / 7.654GiB   33.2MB / 47.4MB
py-v      0.57%     107.6MiB / 7.654GiB   33.2MB / 47.5MB
py-v      0.37%     107.2MiB / 7.654GiB   33.3MB / 47.5MB
py-v      1.67%     107.2MiB / 7.654GiB   33.3MB / 47.5MB
py-v      0.36%     106.9MiB / 7.654GiB   33.3MB / 47.5MB
py-v      0.32%     106.7MiB / 7.654GiB   33.3MB / 47.5MB
py-v      0.31%     106.6MiB / 7.654GiB   33.3MB / 47.5MB
py-v      0.29%     106.6MiB / 7.654GiB   33.3MB / 47.5MB
py-v      0.30%     106.6MiB / 7.654GiB   33.3MB / 47.5MB
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
    ✓ 'rate<0.05' rate=3.04%

    http_req_duration
    ✗ 'p(95)<500' p(95)=4.86s


  █ TOTAL RESULTS 

    checks_total.......: 15720  174.659779/s
    checks_succeeded...: 96.95% 15241 out of 15720
    checks_failed......: 3.04%  479 out of 15720

    ✗ status 200
      ↳  96% — ✓ 15241 / ✗ 479

    CUSTOM
    errors.........................: 3.04%  479 out of 15720

    HTTP
    http_req_duration..............: avg=2.25s    min=1.74ms  med=220.17ms max=1m0s   p(90)=472.77ms p(95)=4.86s   
      { expected_response:true }...: avg=436.76ms min=1.74ms  med=216.67ms max=41.11s p(90)=327.18ms p(95)=710.14ms
    http_req_failed................: 3.04%  479 out of 15720
    http_reqs......................: 15720  174.659779/s

    EXECUTION
    iteration_duration.............: avg=2.26s    min=11.91ms med=231.18ms max=1m0s   p(90)=482.82ms p(95)=4.87s   
    iterations.....................: 15720  174.659779/s
    vus............................: 1      min=1            max=500
    vus_max........................: 500    min=500          max=500

    NETWORK
    data_received..................: 2.2 MB 25 kB/s
    data_sent......................: 1.4 MB 16 kB/s
---
NAME      CPU %     MEM USAGE / LIMIT     NET I/O
py-v      124.13%   129.9MiB / 7.654GiB   37MB / 53.9MB
py-v      112.77%   157.2MiB / 7.654GiB   42.1MB / 62.2MB
py-v      20.32%    133MiB / 7.654GiB   44.2MB / 64.5MB
py-v      0.34%     127MiB / 7.654GiB   45.2MB / 65.8MB
py-v      0.37%     127.5MiB / 7.654GiB   45.6MB / 66.4MB
py-v      0.39%     128.6MiB / 7.654GiB   45.8MB / 66.8MB
py-v      5.02%     129.4MiB / 7.654GiB   45.8MB / 66.9MB
py-v      0.33%     128.5MiB / 7.654GiB   45.9MB / 67.1MB
py-v      0.28%     128.7MiB / 7.654GiB   45.9MB / 67.2MB
py-v      2.04%     129MiB / 7.654GiB   46MB / 67.3MB
py-v      0.33%     128.8MiB / 7.654GiB   46MB / 67.3MB
py-v      0.38%     128.8MiB / 7.654GiB   46MB / 67.3MB
py-v      0.34%     128.9MiB / 7.654GiB   46MB / 67.4MB
py-v      0.37%     129.1MiB / 7.654GiB   46MB / 67.4MB
py-v      0.37%     128.9MiB / 7.654GiB   46MB / 67.4MB
py-v      0.32%     128.9MiB / 7.654GiB   46MB / 67.5MB
py-v      0.31%     128.9MiB / 7.654GiB   46MB / 67.5MB
py-v      1.86%     129.1MiB / 7.654GiB   46MB / 67.5MB
py-v      0.68%     129MiB / 7.654GiB   46MB / 67.5MB
py-v      2.19%     128.6MiB / 7.654GiB   46.1MB / 67.5MB
py-v      0.58%     124.6MiB / 7.654GiB   46.4MB / 67.8MB
py-v      1.22%     120.6MiB / 7.654GiB   46.7MB / 68.2MB
py-v      0.70%     118.6MiB / 7.654GiB   46.8MB / 68.4MB
py-v      3.02%     117.2MiB / 7.654GiB   46.9MB / 68.5MB
py-v      0.27%     117MiB / 7.654GiB   46.9MB / 68.5MB
py-v      0.31%     116.3MiB / 7.654GiB   47MB / 68.5MB
```


high_stress_test: {
    executor: 'constant-vus',
    vus: 1000,
    duration: '1m',
}
не выдержал...