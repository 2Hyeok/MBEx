var idcheck="아이디를 입력하세요";
var passwdck="비밀번호를 입력하세요";
var repasswdck="비밀번호가 다릅니다";
var nameck="이름을 입력하세요";

// 메인 페이지
function maincheck() {
	if(! mainform.id.value){
		alert(idcheck);
		mainform.id.focus();
		return false;
	} else if (! mainform.passwd.value){
		alert(passwdck);
		mainform.passwd.focus();
		return false;
	}
}

// jquery로 갈것이라면 폼마다 이름을 주어야함
/*
$(document).ready(
	function() {
		$("form[name=mainform]")
	}
);
*/

// 가입페이지
function inputcheck() {
	if( ! inputform.id.value ) {
		alert( idcheck );
		inputform.id.focus();
		return false;
	} else if( ! inputform.passwd.value ) {
		alert( passwdck );
		inputform.passwd.focus();
		return false;
	} else if( inputform.passwd.value != inputform.repasswd.value ) {
		alert( repasswdck );
		inputform.repasswd.focus();
		return false;
	} else if( ! inputform.name.value ) {
		alert( nameck );
		inputform.name.focus();
		return false;
	} 
}

// 중복확인
function confirm() {
	if( ! inputform.id.value ) {
		alert( idcheck );
		inputform.id.focus()
	} else {
		url = "confirm" + "?id=" + inputform.id.value 
		open( url, "cofirm", "toolbar=no, menubar=no, scrollbar=no, status=no, width=500, height=300" )
	}
}

// 중복확인 창
function setid(id) {
	// 부모 페이지를 document라고 지정함
	opener.document.inputform.id.value = id;
	window.close();
}
