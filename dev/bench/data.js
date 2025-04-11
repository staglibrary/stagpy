window.BENCHMARK_DATA = {
  "lastUpdate": 1744378124792,
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
          "id": "c68427b39e3df744fdfee946b89ebcc2e904b9e5",
          "message": "Merge pull request #48 from staglibrary/28-passing-data\n\nUpdate C++ wrapper",
          "timestamp": "2023-08-01T15:57:07+01:00",
          "tree_id": "3d05f11aa8225834aed0112e03da3cd6ddfe4c29",
          "url": "https://github.com/staglibrary/stagpy/commit/c68427b39e3df744fdfee946b89ebcc2e904b9e5"
        },
        "date": 1690901940295,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 533.6995959681482,
            "unit": "iter/sec",
            "range": "stddev: 0.00008107042390775321",
            "extra": "mean: 1.8737132415960853 msec\nrounds: 476"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 252.0017254558522,
            "unit": "iter/sec",
            "range": "stddev: 0.000015728588713147536",
            "extra": "mean: 3.9682267976184487 msec\nrounds: 252"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 29.635227109374892,
            "unit": "iter/sec",
            "range": "stddev: 0.00010792502953986127",
            "extra": "mean: 33.743625324999016 msec\nrounds: 200"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 4119.483471548075,
            "unit": "iter/sec",
            "range": "stddev: 0.00000231881716602642",
            "extra": "mean: 242.74888026779885 usec\nrounds: 2539"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 31.550925395764917,
            "unit": "iter/sec",
            "range": "stddev: 0.00013189533933802015",
            "extra": "mean: 31.69479143499956 msec\nrounds: 200"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 26.68264515602735,
            "unit": "iter/sec",
            "range": "stddev: 0.00018556977159736132",
            "extra": "mean: 37.47754370499919 msec\nrounds: 200"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "peter.macgregor@ed.ac.uk",
            "name": "Peter Macgregor",
            "username": "pmacg"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ea37f7746a9eb3430d5747b803874d1604e626ac",
          "message": "Merge pull request #58 from staglibrary/docs-2.0.0\n\nShorten benchmark tests",
          "timestamp": "2024-05-07T12:04:01+01:00",
          "tree_id": "daa4b3570c2f0f76a0b42632a18431629a1731aa",
          "url": "https://github.com/staglibrary/stagpy/commit/ea37f7746a9eb3430d5747b803874d1604e626ac"
        },
        "date": 1715080577096,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 892.8501906651325,
            "unit": "iter/sec",
            "range": "stddev: 0.00002135446967135482",
            "extra": "mean: 1.1200087208975626 msec\nrounds: 713"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 415.5523496059997,
            "unit": "iter/sec",
            "range": "stddev: 0.00002048482384362724",
            "extra": "mean: 2.406435677594258 msec\nrounds: 366"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 176.62160267400165,
            "unit": "iter/sec",
            "range": "stddev: 0.00006210363359708231",
            "extra": "mean: 5.661821571428861 msec\nrounds: 140"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 9667.078221162006,
            "unit": "iter/sec",
            "range": "stddev: 0.000008872109666322985",
            "extra": "mean: 103.44387178029864 usec\nrounds: 3533"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 85.23787363608193,
            "unit": "iter/sec",
            "range": "stddev: 0.00015357308514317978",
            "extra": "mean: 11.731874075947049 msec\nrounds: 79"
          },
          {
            "name": "test/test_performance.py::test_construct_ckns_kde",
            "value": 8.291887308916506,
            "unit": "iter/sec",
            "range": "stddev: 0.0014865716179768814",
            "extra": "mean: 120.59980589999952 msec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_query_ckns_kde",
            "value": 0.062108223871999345,
            "unit": "iter/sec",
            "range": "stddev: 0.14857918763753597",
            "extra": "mean: 16.100927343550016 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_approximate_similarity_graph",
            "value": 0.08231154387718782,
            "unit": "iter/sec",
            "range": "stddev: 0.05692367663467599",
            "extra": "mean: 12.148964202299993 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 68.7579290912779,
            "unit": "iter/sec",
            "range": "stddev: 0.00008001234947543228",
            "extra": "mean: 14.5437771791014 msec\nrounds: 67"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "peter.macgregor@ed.ac.uk",
            "name": "Peter Macgregor",
            "username": "pmacg"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "74b02628e6bfc07d941fe8fe64215c05e4ef9d4c",
          "message": "Merge pull request #62 from staglibrary/59-numpy-matmul\n\nAllow multiplication of SprsMat with numpy array",
          "timestamp": "2024-05-29T15:28:09+01:00",
          "tree_id": "6ab9315cddd37290eadccb5c78ab111b55337d1a",
          "url": "https://github.com/staglibrary/stagpy/commit/74b02628e6bfc07d941fe8fe64215c05e4ef9d4c"
        },
        "date": 1716993587409,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 900.466859423758,
            "unit": "iter/sec",
            "range": "stddev: 0.000019285576389991213",
            "extra": "mean: 1.110535040278925 msec\nrounds: 720"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 419.58711716190567,
            "unit": "iter/sec",
            "range": "stddev: 0.00008400385348679754",
            "extra": "mean: 2.383295289817325 msec\nrounds: 383"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 177.46811652188396,
            "unit": "iter/sec",
            "range": "stddev: 0.00005729730570912932",
            "extra": "mean: 5.634814971830098 msec\nrounds: 142"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 9653.695376548445,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036869034683574704",
            "extra": "mean: 103.58727523444365 usec\nrounds: 3517"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 84.75337300811839,
            "unit": "iter/sec",
            "range": "stddev: 0.00005990388490023737",
            "extra": "mean: 11.798940437499894 msec\nrounds: 80"
          },
          {
            "name": "test/test_performance.py::test_construct_ckns_kde",
            "value": 9.720372305092363,
            "unit": "iter/sec",
            "range": "stddev: 0.0015672040486595384",
            "extra": "mean: 102.87671795000222 msec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_query_ckns_kde",
            "value": 0.06517199670962653,
            "unit": "iter/sec",
            "range": "stddev: 0.045035234062359306",
            "extra": "mean: 15.3440135409 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_approximate_similarity_graph",
            "value": 0.0835793663078013,
            "unit": "iter/sec",
            "range": "stddev: 0.04427878908038771",
            "extra": "mean: 11.96467554345001 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 68.14309306784924,
            "unit": "iter/sec",
            "range": "stddev: 0.0002423757893833872",
            "extra": "mean: 14.675001602940336 msec\nrounds: 68"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "prm4@st-andrews.ac.uk",
            "name": "Peter Macgregor"
          },
          "committer": {
            "email": "prm4@st-andrews.ac.uk",
            "name": "Peter Macgregor"
          },
          "distinct": true,
          "id": "2638be80393ef588aff3330a82411618a07d4bdb",
          "message": "Don't rebuild swig for benchmark",
          "timestamp": "2024-07-09T11:30:52+01:00",
          "tree_id": "f4b1c55534674d76cd9c63c226895e4ff3cde192",
          "url": "https://github.com/staglibrary/stagpy/commit/2638be80393ef588aff3330a82411618a07d4bdb"
        },
        "date": 1720521761594,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 891.744374558128,
            "unit": "iter/sec",
            "range": "stddev: 0.000025734753933409685",
            "extra": "mean: 1.1213975983818392 msec\nrounds: 742"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 426.3852521593481,
            "unit": "iter/sec",
            "range": "stddev: 0.000022511321265729746",
            "extra": "mean: 2.34529687632414 msec\nrounds: 283"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 173.99875100691582,
            "unit": "iter/sec",
            "range": "stddev: 0.000041202921718027426",
            "extra": "mean: 5.7471676906476965 msec\nrounds: 139"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 9471.66103618059,
            "unit": "iter/sec",
            "range": "stddev: 0.000006664048549454151",
            "extra": "mean: 105.57810252923134 usec\nrounds: 3638"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 84.41373828329448,
            "unit": "iter/sec",
            "range": "stddev: 0.00006891479747746496",
            "extra": "mean: 11.846412922076459 msec\nrounds: 77"
          },
          {
            "name": "test/test_performance.py::test_construct_ckns_kde",
            "value": 8.932469689939351,
            "unit": "iter/sec",
            "range": "stddev: 0.0020434433854748585",
            "extra": "mean: 111.95112154998981 msec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_query_ckns_kde",
            "value": 0.06454251880945648,
            "unit": "iter/sec",
            "range": "stddev: 0.05581585739715181",
            "extra": "mean: 15.493662448350008 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_approximate_similarity_graph",
            "value": 0.08329625095406638,
            "unit": "iter/sec",
            "range": "stddev: 0.04228928759417283",
            "extra": "mean: 12.005342239850012 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 69.32165998908,
            "unit": "iter/sec",
            "range": "stddev: 0.00012285621715710975",
            "extra": "mean: 14.42550568116122 msec\nrounds: 69"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "prm4@st-andrews.ac.uk",
            "name": "Peter Macgregor",
            "username": "pmacg"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f1cbaedc3546d570024612e98d029e9cb640ae99",
          "message": "Merge pull request #73 from staglibrary/release-2.1.1\n\nUpdate release 2.1.1",
          "timestamp": "2025-04-11T12:17:23+01:00",
          "tree_id": "286c97da6db1721cb687d0b76497a6596cc8599c",
          "url": "https://github.com/staglibrary/stagpy/commit/f1cbaedc3546d570024612e98d029e9cb640ae99"
        },
        "date": 1744370943791,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 707.5679450663919,
            "unit": "iter/sec",
            "range": "stddev: 0.000050333000672964296",
            "extra": "mean: 1.4132918357489597 msec\nrounds: 621"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 352.9622761402675,
            "unit": "iter/sec",
            "range": "stddev: 0.00003317955273779746",
            "extra": "mean: 2.8331639599995078 msec\nrounds: 350"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 177.65931364503888,
            "unit": "iter/sec",
            "range": "stddev: 0.00010746652022027151",
            "extra": "mean: 5.628750778571552 msec\nrounds: 140"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 10170.051980357675,
            "unit": "iter/sec",
            "range": "stddev: 0.000004171803612033073",
            "extra": "mean: 98.32791434413402 usec\nrounds: 3911"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 87.71506046718136,
            "unit": "iter/sec",
            "range": "stddev: 0.00007576961182180199",
            "extra": "mean: 11.400550768293098 msec\nrounds: 82"
          },
          {
            "name": "test/test_performance.py::test_construct_ckns_kde",
            "value": 9.596148393151848,
            "unit": "iter/sec",
            "range": "stddev: 0.0018380677341218784",
            "extra": "mean: 104.20847604999892 msec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_query_ckns_kde",
            "value": 0.06418151977640774,
            "unit": "iter/sec",
            "range": "stddev: 0.08341031111074874",
            "extra": "mean: 15.580808984950005 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_approximate_similarity_graph",
            "value": 0.08292453397940577,
            "unit": "iter/sec",
            "range": "stddev: 0.040395392471609746",
            "extra": "mean: 12.059157308599998 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 71.64169458676525,
            "unit": "iter/sec",
            "range": "stddev: 0.00008531631943007261",
            "extra": "mean: 13.958352126761882 msec\nrounds: 71"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "prm4@st-andrews.ac.uk",
            "name": "Peter Macgregor",
            "username": "pmacg"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "fe1e181ff76550cfdac004dcbc48b13ae7b26a47",
          "message": "Merge pull request #75 from staglibrary/release-2.1.1\n\nFix artifacts in github actions for 2.1.1",
          "timestamp": "2025-04-11T14:16:48+01:00",
          "tree_id": "ea2541e742cab4a6b16ac3797e7e880809351737",
          "url": "https://github.com/staglibrary/stagpy/commit/fe1e181ff76550cfdac004dcbc48b13ae7b26a47"
        },
        "date": 1744378123670,
        "tool": "pytest",
        "benches": [
          {
            "name": "test/test_performance.py::test_sbm",
            "value": 929.703094570332,
            "unit": "iter/sec",
            "range": "stddev: 0.00006609054183051311",
            "extra": "mean: 1.0756122097906493 msec\nrounds: 715"
          },
          {
            "name": "test/test_performance.py::test_load_edgelist",
            "value": 362.5027992451656,
            "unit": "iter/sec",
            "range": "stddev: 0.00006389606683280424",
            "extra": "mean: 2.758599387597243 msec\nrounds: 387"
          },
          {
            "name": "test/test_performance.py::test_spectral_cluster",
            "value": 176.3803230868197,
            "unit": "iter/sec",
            "range": "stddev: 0.00010007187895953172",
            "extra": "mean: 5.669566664234819 msec\nrounds: 137"
          },
          {
            "name": "test/test_performance.py::test_local_cluster",
            "value": 10041.596037279984,
            "unit": "iter/sec",
            "range": "stddev: 0.000004939416247235211",
            "extra": "mean: 99.58576269025805 usec\nrounds: 3940"
          },
          {
            "name": "test/test_performance.py::test_compute_eigensystem",
            "value": 87.28890593815039,
            "unit": "iter/sec",
            "range": "stddev: 0.00009122998811831145",
            "extra": "mean: 11.456209575000997 msec\nrounds: 80"
          },
          {
            "name": "test/test_performance.py::test_construct_ckns_kde",
            "value": 9.028965572997524,
            "unit": "iter/sec",
            "range": "stddev: 0.0035848458200206613",
            "extra": "mean: 110.75465865000638 msec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_query_ckns_kde",
            "value": 0.06298661235284081,
            "unit": "iter/sec",
            "range": "stddev: 0.08475714599089051",
            "extra": "mean: 15.876389642900017 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_approximate_similarity_graph",
            "value": 0.08269214581017156,
            "unit": "iter/sec",
            "range": "stddev: 0.04238533921442788",
            "extra": "mean: 12.0930469297 sec\nrounds: 20"
          },
          {
            "name": "test/test_performance.py::test_lap_eigvecs",
            "value": 70.46127640333474,
            "unit": "iter/sec",
            "range": "stddev: 0.00024677085316457116",
            "extra": "mean: 14.192192521120337 msec\nrounds: 71"
          }
        ]
      }
    ]
  }
}