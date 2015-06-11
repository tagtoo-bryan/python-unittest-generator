# python-unittest-generator
Auto generating unit testing file and description for python class

******

#### schema format

```
name: "name of module"
path: "path for module"
tests:
    "name of tested method":
        test_instances:
            - args: [arg1, arg2, ...]
            - kwargs: {kwarg1: value1, kwarg2, value2, ......}
            - checktype: "Equal"
    ...
```


******

#### How to use

python unittest-generator.py

===


#### Motivation (from [george](https://github.com/georgefs))

DDT
===

TDD 在我們小公司的狀況之下可能不太實際, 面對每天需求快速變動, 規格一直修正的連續性狀況, 要用 測試導向開發 會有一定的困難, 所以我提出了 DDT 的開發模式

develop -> debug -> test

這樣我們在開發好一個版本後再去建立 test case, 這樣可以避免需求不斷變換, 程式和測試都需要同時修改的窘境..  

這樣就造成令一個問題, 我們功能都開發好, 也手動debug 過了, 程式大體上穩定, 這時候我們回頭寫 test case 感覺就很蠢..  面對一個正常穩定的程式碼在寫他的 test case, 我們必須要反覆的 try and error 取得程式輸出.. 但是, 我們在debug 的過程當中其實已經有作過測試了.. 所以反覆作這些問題其實會很煩..

所以簡單來說這次要做的就是要 **自動** 產生 **穩定code的** test case 的 framework

解決方案
---

其實在debug 過後我們基本上可以大致上說明程式基本正確, 但是要補test case, 就需要反覆回去取output, 

我希望能夠只要定義好 需要 test 的method & input , 就可以快速產生 test case

	肯定會有人問, 這樣怎麼產生test case.. 沒有output 阿.. 嗯.. 要用這樣的pattern 有一個先決條件, 
	就是目前功能基本上穩定正常！！, 所以 output 基本上用 method(input) 就應該可以取得！！這樣我們只要
	知道我們想測試的函數名稱, 還有要測試的input, 那我們就可以快速產生 test case 了！！

概念上就是針對一個已經正常的程式我們要如何快速產生unit test

issues
---

1. output excepiton 需要處理（如果該input 進去出來是exception, 那我們產出的test case 也是要能夠控制的） 
2. many datatype(輸入和輸出可能會有很多不同的class instance, 這部份要如何處理？)
3. api server（針對http server 我們也需要能夠產生test case##不過這應該是plugin）
4. mock object(基本上我們寫test case時會希望測試的過程足夠乾淨而使用mock, 避免變因太多, 那在這部份我們作這framwork 要如何自動mock?)
5. 由於程式開發不可避免錯誤, 我們要如何在產生test case 後也同時能確認我們的程式正確？




