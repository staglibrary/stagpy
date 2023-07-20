window.BENCHMARK_DATA = {
  "lastUpdate": 1689848233363,
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
          "id": "060cef0f56f12617e026e4625e698d7f8cf08ba4",
          "message": "Merge pull request #42 from staglibrary/performance-tests\n\nUpdate + add performance tests",
          "timestamp": "2023-07-14T14:32:27+01:00",
          "tree_id": "7c427c094f2085c3b23fd65241a16d5e937d4ee4",
          "url": "https://github.com/staglibrary/stagpy/commit/060cef0f56f12617e026e4625e698d7f8cf08ba4"
        },
        "date": 1689341644474,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 492.9932519696395,
            "unit": "iter/sec",
            "range": "stddev: 0.00002830995458965877",
            "extra": "mean: 2.0284253303767 msec\nrounds: 451"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 319.87596920318117,
            "unit": "iter/sec",
            "range": "stddev: 0.00002717402354069187",
            "extra": "mean: 3.1262117079036114 msec\nrounds: 291"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 31.575804595926265,
            "unit": "iter/sec",
            "range": "stddev: 0.0001829846102771895",
            "extra": "mean: 31.66981848275735 msec\nrounds: 29"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 4527.474413887868,
            "unit": "iter/sec",
            "range": "stddev: 0.000025130750785153165",
            "extra": "mean: 220.8736943786 usec\nrounds: 2526"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 40.42022089543686,
            "unit": "iter/sec",
            "range": "stddev: 0.002302603202413194",
            "extra": "mean: 24.740092405405246 msec\nrounds: 37"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 31.985561909264497,
            "unit": "iter/sec",
            "range": "stddev: 0.0018048477385145191",
            "extra": "mean: 31.26410606250296 msec\nrounds: 32"
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
          "id": "843f049d62a468d398872ef3fcfb3f386d74c35d",
          "message": "Merge pull request #45 from staglibrary/44-bug-in-personalised-pagerank\n\nCheck for empty matrix when converting from SprsMat to scipy",
          "timestamp": "2023-07-19T18:25:09+01:00",
          "tree_id": "bac02dba62a9010d1e719973225c6988e4ae3964",
          "url": "https://github.com/staglibrary/stagpy/commit/843f049d62a468d398872ef3fcfb3f386d74c35d"
        },
        "date": 1689787656120,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 388.1304415074423,
            "unit": "iter/sec",
            "range": "stddev: 0.0007088118363614209",
            "extra": "mean: 2.5764534111680217 msec\nrounds: 197"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 183.7535953964835,
            "unit": "iter/sec",
            "range": "stddev: 0.0013318246386874203",
            "extra": "mean: 5.442070386934792 msec\nrounds: 199"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 20.076255302389015,
            "unit": "iter/sec",
            "range": "stddev: 0.006740607832236479",
            "extra": "mean: 49.81008584210438 msec\nrounds: 19"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 3143.389905601551,
            "unit": "iter/sec",
            "range": "stddev: 0.00017036950249658698",
            "extra": "mean: 318.127890599251 usec\nrounds: 2404"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 18.388120566172454,
            "unit": "iter/sec",
            "range": "stddev: 0.009461984778451766",
            "extra": "mean: 54.38293687499751 msec\nrounds: 16"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 15.337557744832964,
            "unit": "iter/sec",
            "range": "stddev: 0.009951338722496018",
            "extra": "mean: 65.19942852941419 msec\nrounds: 17"
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
          "id": "4fa5c56d609c695a5548e495a47a3b3b699ac5d4",
          "message": "Run at least 200 rounds for each performance test",
          "timestamp": "2023-07-20T11:10:51+01:00",
          "tree_id": "f310f42d2c0938271ee730b3225bef6b87a9b13e",
          "url": "https://github.com/staglibrary/stagpy/commit/4fa5c56d609c695a5548e495a47a3b3b699ac5d4"
        },
        "date": 1689848024837,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 557.1023970744282,
            "unit": "iter/sec",
            "range": "stddev: 0.000025729142203802123",
            "extra": "mean: 1.7950021490688384 msec\nrounds: 483"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 301.0599389999985,
            "unit": "iter/sec",
            "range": "stddev: 0.000009799190449689856",
            "extra": "mean: 3.3215976968626335 msec\nrounds: 287"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 29.294491730032462,
            "unit": "iter/sec",
            "range": "stddev: 0.0001365642894922592",
            "extra": "mean: 34.1361102700003 msec\nrounds: 200"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 4208.775521076471,
            "unit": "iter/sec",
            "range": "stddev: 0.000002758700784756464",
            "extra": "mean: 237.59879684536654 usec\nrounds: 2599"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 37.755712151548956,
            "unit": "iter/sec",
            "range": "stddev: 0.0023117544185850096",
            "extra": "mean: 26.486058480000736 msec\nrounds: 200"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 29.625366934332632,
            "unit": "iter/sec",
            "range": "stddev: 0.0026843965819186803",
            "extra": "mean: 33.75485617500004 msec\nrounds: 200"
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
          "id": "15866cc0c0ca6503bc2bf7dcb85b883a50c52b8f",
          "message": "Merge pull request #46 from staglibrary/performance-tests\n\nRun at least 200 rounds for each performance test",
          "timestamp": "2023-07-20T11:14:37+01:00",
          "tree_id": "e009e6844fc838493883e1535c1d0d0011274d8d",
          "url": "https://github.com/staglibrary/stagpy/commit/15866cc0c0ca6503bc2bf7dcb85b883a50c52b8f"
        },
        "date": 1689848231805,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 492.18603569108325,
            "unit": "iter/sec",
            "range": "stddev: 0.00003750656427612335",
            "extra": "mean: 2.0317520764194175 msec\nrounds: 458"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 319.99866442660516,
            "unit": "iter/sec",
            "range": "stddev: 0.000012279756177442357",
            "extra": "mean: 3.1250130427633698 msec\nrounds: 304"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 31.922672117749595,
            "unit": "iter/sec",
            "range": "stddev: 0.00011270505377068736",
            "extra": "mean: 31.325698434999794 msec\nrounds: 200"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 4387.112580005332,
            "unit": "iter/sec",
            "range": "stddev: 0.00002554260616115601",
            "extra": "mean: 227.9403552481401 usec\nrounds: 2601"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 38.52861740683091,
            "unit": "iter/sec",
            "range": "stddev: 0.0022038773945031024",
            "extra": "mean: 25.954733579998788 msec\nrounds: 200"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 30.900357324516623,
            "unit": "iter/sec",
            "range": "stddev: 0.0020185079245287917",
            "extra": "mean: 32.36208531500026 msec\nrounds: 200"
          }
        ]
      }
    ]
  }
}