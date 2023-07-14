window.BENCHMARK_DATA = {
  "lastUpdate": 1689341497939,
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
      },
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
          "id": "f223387f3087698928c6a8fd5d537e8523977f2d",
          "message": "Add local clustering performance test",
          "timestamp": "2023-07-14T14:26:46+01:00",
          "tree_id": "8bb8c443ddda17280282f4bb546d39308ad0508e",
          "url": "https://github.com/staglibrary/stagpy/commit/f223387f3087698928c6a8fd5d537e8523977f2d"
        },
        "date": 1689341315787,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 528.1505068991445,
            "unit": "iter/sec",
            "range": "stddev: 0.0003348121938083998",
            "extra": "mean: 1.8933996785710927 msec\nrounds: 336"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 279.06006031790076,
            "unit": "iter/sec",
            "range": "stddev: 0.00040761139659823933",
            "extra": "mean: 3.5834579798370854 msec\nrounds: 248"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 28.133086298854384,
            "unit": "iter/sec",
            "range": "stddev: 0.0010996157134594443",
            "extra": "mean: 35.54533581481678 msec\nrounds: 27"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 4163.488477619118,
            "unit": "iter/sec",
            "range": "stddev: 0.00004852682022428154",
            "extra": "mean: 240.1832034303714 usec\nrounds: 2915"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 24.647186780522276,
            "unit": "iter/sec",
            "range": "stddev: 0.00319672977905899",
            "extra": "mean: 40.57258172726883 msec\nrounds: 22"
          }
        ]
      },
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
          "id": "022588c750eeba946024e1e9dcaa7e6271c112d1",
          "message": "Add compute eigensystem perf test",
          "timestamp": "2023-07-14T14:29:54+01:00",
          "tree_id": "54c4a2ff2a1fc0b79fefa1385ab4d4d5d6fde0f1",
          "url": "https://github.com/staglibrary/stagpy/commit/022588c750eeba946024e1e9dcaa7e6271c112d1"
        },
        "date": 1689341496672,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 554.8879692793779,
            "unit": "iter/sec",
            "range": "stddev: 0.000023404073961226265",
            "extra": "mean: 1.802165581817678 msec\nrounds: 495"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 302.17371137301876,
            "unit": "iter/sec",
            "range": "stddev: 0.000014740865807531509",
            "extra": "mean: 3.309354726644465 msec\nrounds: 289"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 29.490034385812674,
            "unit": "iter/sec",
            "range": "stddev: 0.00024071302466265824",
            "extra": "mean: 33.90976039285626 msec\nrounds: 28"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 4191.108061886573,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023765544670311305",
            "extra": "mean: 238.60038568174335 usec\nrounds: 2598"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 37.51512521577956,
            "unit": "iter/sec",
            "range": "stddev: 0.0021629478230264293",
            "extra": "mean: 26.65591529411666 msec\nrounds: 34"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 29.43502810318306,
            "unit": "iter/sec",
            "range": "stddev: 0.002263233308958793",
            "extra": "mean: 33.97312876667039 msec\nrounds: 30"
          }
        ]
      }
    ]
  }
}