window.BENCHMARK_DATA = {
  "lastUpdate": 1689334210933,
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
      }
    ]
  }
}