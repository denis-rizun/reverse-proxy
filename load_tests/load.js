import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
    scenarios: {
        // low_load: {
        //     executor: 'constant-vus',
        //     vus: 10,
        //     duration: '30s',
        // },
        // medium_load: {
        //     executor: 'constant-vus',
        //     vus: 50,
        //     duration: '1m',
        // },
        // high_load: {
        //     executor: 'constant-vus',
        //     vus: 100,
        //     duration: '1m',
        // },
        // stress_test: {
        //     executor: 'constant-vus',
        //     vus: 500,
        //     duration: '1m',
        // },
        // high_stress_test: {
        //     executor: 'constant-vus',
        //     vus: 1000,
        //     duration: '1m',
        // }
    },
    thresholds: {
        'http_req_duration': ['p(95)<500'],
        'errors': ['rate<0.05'],
    },
};

export default function () {
    let res = http.get('http://localhost:8000/api/test?id=1');

    let success = check(res, {
        'status 200': (r) => r.status === 200,
    });
    errorRate.add(!success);

    sleep(0.01);
}