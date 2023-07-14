window.BENCHMARK_DATA = {
  "lastUpdate": 1689340594139,
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
          "id": "a7bfaf91a609537ed77d8f03a13f9b64cc0cc872",
          "message": "Make performance tests more consistent",
          "timestamp": "2023-07-14T14:14:14+01:00",
          "tree_id": "999151dfa9ab4bffb23d0942b29d0eb39ee61567",
          "url": "https://github.com/staglibrary/stagpy/commit/a7bfaf91a609537ed77d8f03a13f9b64cc0cc872"
        },
        "date": 1689340592604,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 447.57195254323085,
            "unit": "iter/sec",
            "range": "stddev: 0.0002105191454244264",
            "extra": "mean: 2.234277626910525 msec\nrounds: 327"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 225.49977003369003,
            "unit": "iter/sec",
            "range": "stddev: 0.0004719147088082275",
            "extra": "mean: 4.434594322870477 msec\nrounds: 223"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 24.010325568479963,
            "unit": "iter/sec",
            "range": "stddev: 0.0025038591284407266",
            "extra": "mean: 41.648748041666295 msec\nrounds: 24"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 19.199036566748063,
            "unit": "iter/sec",
            "range": "stddev: 0.0037593525896426104",
            "extra": "mean: 52.08594694443983 msec\nrounds: 18"
          }
        ]
      }
    ]
  }
}