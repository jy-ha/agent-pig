<h1>Agent Pig</h1>

Daily food selection service based on naive bayesian.    
Demo : https://blonix.dev/agentpig    
본 repository는 해당 서비스 backend의 core script만을 다루며, 전체 Docker Container를 제공하지 않습니다.

<h2>Project details</h2>

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>
<br/>

|||
|---|---|
|Period|2021.11 ~ 2021.12|
|Team|None|

주어지는 각 메뉴에 대한 호불호를 입력하면 최종적으로 가장 확률이 높은 메뉴를 선정합니다.    
스무고개와 유사한 Naive bayesian 알고리즘을 적용하였습니다.

<h2>Limitation</h2>

1. 메뉴의 수가 많아질수록 matrix의 크기가 급격히 커지고 연산량도 많아집니다.
2. matrix를 파일로 저장하지만, service 실행중에는 상시 memory load 되어 있으므로,
웹엔진에서 멀티 프로세스 기능을 활용하거나 load-balancer 등으로 다수의 인스턴스가 실행될 시 정상작동 하지 않습니다.
이를 해결하기 위해 모든 요청마다 matrix 파일을 읽고쓰는 방법으로 해결할 수 있습니다.
3. Naive bayesian은 각 사건이 독립사건이라 전제하지만, 해당 문제에서는 적절하지 못한 가정일 수 있습니다. 개선을 위해 Recommandation Algorism의 적용을 고려해볼 수 있습니다.
