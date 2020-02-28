# 0. 프로젝트 명(Project Title)
<h3>영상처리와 딥러닝을 이용한 악보 코드 변환 프로그램 - OurChord</h3> 
Music Score Chord Conversion Program using OpenCV, DeepLearning.(ver. 2020 Capston Design)

# 1. 개요(Introduction)
* 음악 전공자가 아닌 사람들은 조표(샾, 플랫)가 많은 악보를 연주함에 어려움을 느끼는 경우 많음 <br>
  People who are not music majosr often find it difficult to play music with lots of key signature.
* 세션 연주자들은 각자 악기에 맞추어 하나의 코드(chord)로 맞추어 연주해야 하는 경우 많음 <br>
  Session performers often have to play one chord to each instrument.
* 대부분의 악보가 PDF 파일로 제공되어 악보 수정이 어려움 <br>
  Most of the score are provided in PDF files, making it difficult to modify the notes.
# 2. 제작목적(Proposal)
* 조 옮김을 통한 연주하기 쉬운 악보 제공으로 악기 연주 시 자신감 부여 <br>
  Chord Conversion to provide easy to play sheet music to give confidence in playing musical instruments.
* 세션 연주자들에게 서로 악기의 코드(chord)를 빠르고 쉽게 바꿀 수 있도록 함 <br>
  Make it quick and easy for session performers to chord conversion of their instruments.
* 악보 수정이 용이한 MIDI 파일 제공 <br>
  Provide easy to modify MIDI files.
# 3. 주요기능(Main Function)
* PDF 악보 파일 MIDI 파일 변환 제공 <br>
 Provide convert the PDF music score file to a MIDI file.
* 사용자가 원하는 코드(chord)의 MIDI 파일 제공 <br>
  Provide a MIDI file of desired chord.
* 악기 튜닝 시 원하는 코드(chord) 음 제공 <br>
  Provide the desired sound of the chord when tuning the instrument.
# 4. 역할분담(Role)
* 임영규 : Application 환경 설계
* 김민지 : Server 환경 설계
* 문지수 : Database 환경 설계
* 공동 : 딥러닝 모델 구현
# 5. Detail
* Library : Tensorflow, OpenCV
* Tool : Pychram CE, Visual Studio Code, Android Studio, MySQLWorkbench
* Language : Python, Java
* ETC : PHP, MYSQL
* Server/Database : Linux, MYSQL
