window.BENCHMARK_DATA = {
  "lastUpdate": 1689335013365,
  "repoUrl": "https://github.com/staglibrary/stagpy",
  "entries": {
    "Performance Tests": [
      {
        "commit": {
          "author": {
            "email": "peter.macgregor@ed.ac.uk",
            "name": "Peter Macgregor"
          },
          "committer": {
            "email": "peter.macgregor@ed.ac.uk",
            "name": "Peter Macgregor"
          },
          "distinct": true,
          "id": "92ba076a14adfa4741b8e07769c6c2bb076acced",
          "message": "Run workflow on performance-tests branch",
          "timestamp": "2023-07-14T12:15:47+01:00",
          "tree_id": "6ea95d7ba1725af7d8d7c7b7112990efa32aead0",
          "url": "https://github.com/staglibrary/stagpy/commit/92ba076a14adfa4741b8e07769c6c2bb076acced"
        },
        "date": 1689334209996,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_typical_small_sbm",
            "value": 472.86286279236447,
            "unit": "iter/sec",
            "range": "stddev: 0.00006658479746019196",
            "extra": "mean: 2.1147780438809867 msec\nrounds: 433"
          },
          {
            "name": "test/test_performance.py::test_typical_large_sbm",
            "value": 2.5560009063375455,
            "unit": "iter/sec",
            "range": "stddev: 0.0542112966056682",
            "extra": "mean: 391.236167999989 msec\nrounds: 5"
          },
          {
            "name": "test/test_performance.py::test_sc_small",
            "value": 22.793501701496503,
            "unit": "iter/sec",
            "range": "stddev: 0.0015434102376278038",
            "extra": "mean: 43.87215326087195 msec\nrounds: 23"
          },
          {
            "name": "test/test_performance.py::test_sc_large",
            "value": 0.1464743155030448,
            "unit": "iter/sec",
            "range": "stddev: 0.3478897954574868",
            "extra": "mean: 6.827135505400008 sec\nrounds: 5"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 0.09729287820785815,
            "unit": "iter/sec",
            "range": "stddev: 7.570405168804506",
            "extra": "mean: 10.2782445994 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "macgregor.pr@gmail.com",
            "name": "Peter Macgregor",
            "username": "pmacg"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "7b8121d3543b20c2265fa21ac938f2cd306b875b",
          "message": "Merge pull request #40 from staglibrary/performance-tests\n\nRun benchmarks on main branch",
          "timestamp": "2023-07-14T12:37:23+01:00",
          "tree_id": "af73274b864fe6ea3fb4ca4c4f29c7b2b5153705",
          "url": "https://github.com/staglibrary/stagpy/commit/7b8121d3543b20c2265fa21ac938f2cd306b875b"
        },
        "date": 1689335012010,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_typical_small_sbm",
            "value": 458.11562778533397,
            "unit": "iter/sec",
            "range": "stddev: 0.00031164743452416786",
            "extra": "mean: 2.182855024689498 msec\nrounds: 405"
          },
          {
            "name": "test/test_performance.py::test_typical_large_sbm",
            "value": 2.304724633273197,
            "unit": "iter/sec",
            "range": "stddev: 0.05399120804946403",
            "extra": "mean: 433.89131419999103 msec\nrounds: 5"
          },
          {
            "name": "test/test_performance.py::test_sc_small",
            "value": 20.255791348495812,
            "unit": "iter/sec",
            "range": "stddev: 0.004143937408910184",
            "extra": "mean: 49.368597000001174 msec\nrounds: 22"
          },
          {
            "name": "test/test_performance.py::test_sc_large",
            "value": 0.08998574314118027,
            "unit": "iter/sec",
            "range": "stddev: 0.45661206200074334",
            "extra": "mean: 11.112871496000002 sec\nrounds: 5"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 0.04471589297028851,
            "unit": "iter/sec",
            "range": "stddev: 23.32488326781903",
            "extra": "mean: 22.363413399000002 sec\nrounds: 5"
          }
        ]
      }
    ]
  }
}