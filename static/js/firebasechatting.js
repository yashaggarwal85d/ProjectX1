const SelectedChatDiv = document.getElementById('selectchat');
const NoChatDiv = document.getElementById('nochat');
const wrapper = document.getElementById('list-wrapper');
const Textbox_wrapper = document.getElementById('form-wrapper');
const chatList = document.getElementById('chat_list');
const user = chatList.classList.value;
const IssueTime = document.getElementsByClassName('issue_time');
const IssueLastMessage = document.getElementsByClassName('issue_lastmessage');
const ProjectTime = document.getElementsByClassName('project_time');
const ProjectLastMessage = document.getElementsByClassName('project_lastmessage');

class chat {

    initialize(userid, senderid) {
        this.isactive = true;
        this.user_id = userid;
        this.sender_id = senderid;
        this.search_message = "";
        this.loadchat();
    }

    loadchat() {
        if (SelectedChatDiv.classList.contains('hide')) {
            SelectedChatDiv.classList.remove('hide');
            NoChatDiv.classList.add('hide');
        }
        this.buildchat();
    }

    buildDockey() {
        if (this.user_id < this.sender_id)
            var dockey = String(this.user_id) + ":" + String(this.sender_id);
        else
            var dockey = String(this.sender_id) + ":" + String(this.user_id);

        return dockey
    }

    sendMessage = async (msg) => {
        if (msg != "") {
            await
            firebase
                .firestore()
                .collection('chats')
                .doc(this.buildDockey())
                .update({
                    messages: firebase.firestore.FieldValue.arrayUnion({
                        sender: this.sender_id,
                        message: msg,
                        timestamp: Date.now()
                    }),
                    receiverHasRead: false
                });
        }
    }

    buildProfile() {

        const ProfilePic = document.getElementById('chat_instance_profile_pic');
        const ProfileName = document.getElementById(`chat_instance_profile_name`);
        const ProfileSkills = document.getElementById('userskills');

        var url = `http://127.0.0.1:8000/accounts/profile_api/${this.user_id}/`;
        $.get(url, (data) => {

            ProfilePic.src = data.profile_pic;
            ProfileName.innerHTML = data.first_name + " " + data.last_name;
            ProfileSkills.innerHTML = data.occupation + " | Works At " + data.works_at;
        })
    }

    searchfunc = async (e) => {
        this.search_message = e;
        this.buildchat();
    }

    buildchat = async () => {
        const firebaseRef = firebase.firestore().collection('chats').doc(this.buildDockey());

        firebaseRef.onSnapshot((value) => {
            if (typeof value.data() != "undefined") {

                var filterArray = value.data().users.filter(_user => _user == this.user_id)[0].split('')[0];

                this.messages = value.data().messages;
                var message;
                var item = "";

                if (this.user_id == filterArray && this.isactive) {
                    for (message of this.messages) {
                        const time = moment(message.timestamp).fromNow();
                        if (this.search_message !== "" && message.message.indexOf(this.search_message) === -1) {} else {

                            if (message.sender == this.sender_id)
                                item += `<div id="data-row" class="message message-right">
                                            <div class="message-body">
                                                <div class="message-row">
                                                    <div class="d-flex align-items-center justify-content-end">

                                                        <div class="message-content bg-primary text-white">
                                                            <div>${message.message}</div>

                                                            <div class="mt-1">
                                                                <small class="opacity-65">${time}</small>
                                                            </div>
                                                        </div>
                                                        <!-- Message: content -->

                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    `
                            else
                                item += `<div id="data-row" class="message">
                                            <div class="message-body">

                                                <div class="message-row">
                                                    <div class="d-flex align-items-center">
                                                        <a class="edit"></span></a>
                                                        <a class="delete"></a>
                                                        

                                                        <!-- Message: content -->
                                                        <div class="message-content bg-light">
                                                            <div>${message.message}</div>

                                                            <div class="mt-1">
                                                                <small class="opacity-65">${time}</small>
                                                            </div>
                                                        </div>
                                                        
                                                    </div>
                                                </div>
                                                <!-- Message: row -->

                                            </div>
                                            <!-- Message: Body -->
                                        </div>
                                    `
                        }
                    }

                    wrapper.innerHTML = item;
                }
                this.ScrollToEnd();
            } else {
                this.newChatSubmit();
            }
        });
        this.buildProfile();
    }

    newChatSubmit = async () => {
        await
        firebase
            .firestore()
            .collection('chats')
            .doc(this.buildDockey())
            .set({
                messages: [{
                    message: "hi",
                    sender: this.sender_id,
                    timestamp: Date.now()
                }],
                users: [String(this.sender_id), String(this.user_id)],
                receiverHasRead: false
            })
    }

    ScrollToEnd = () => {
        const container = document.getElementById('chatview-container');
        if (container)
            container.scrollTo(0, container.scrollHeight);
    }

}

class Issuechat {

    initialize(issueid, senderid) {
        this.isactive = true;
        this.issue_id = String(issueid);
        this.sender_id = senderid;
        this.search_message = "";
        this.loadchat();
    }

    loadchat() {
        if (SelectedChatDiv.classList.contains('hide')) {
            SelectedChatDiv.classList.remove('hide');
            NoChatDiv.classList.add('hide');
        }
        this.buildchat();
    }

    sendMessage = async (msg) => {
        if (msg != "") {
            await
            firebase
                .firestore()
                .collection('issues')
                .doc(this.issue_id)
                .update({
                    messages: firebase.firestore.FieldValue.arrayUnion({
                        sender: this.sender_id,
                        message: msg,
                        timestamp: Date.now()
                    }),
                });
        }
    }

    buildIssue() {

        const ProfilePic = document.getElementById('chat_instance_profile_pic');
        const ProfileName = document.getElementById(`chat_instance_profile_name`);
        const ProfileSkills = document.getElementById('userskills');

        var url = `http://127.0.0.1:8000/issues/issue_detail_api/${this.issue_id}/`;
        $.get(url, (data) => {

            ProfilePic.src = `https://picsum.photos/id/${this.issue_id}/200/300`;
            ProfileName.innerHTML = data.name;
            ProfileSkills.innerHTML = "Deadline " + data.deadline + " | Priority " + data.priority;
        })
    }

    searchfunc = async (e) => {
        this.search_message = e;
        this.buildchat();
    }

    buildchat = async () => {
        const firebaseRef = firebase.firestore().collection('issues').doc(this.issue_id);

        firebaseRef.onSnapshot((value) => {
            if (typeof value.data() != "undefined") {

                //var filterArray = value.data().users.filter(_user => _user == this.user_id)[0].split('')[0];

                this.messages = value.data().messages;
                var message;
                var item = "";

                if (this.issue_id == value.data().issue && this.isactive) {
                    for (message of this.messages) {
                        const time = moment(message.timestamp).fromNow();
                        if (this.search_message !== "" && message.message.indexOf(this.search_message) === -1) {} else {

                            if (message.sender == this.sender_id)
                                item += `<div class="message message-right">
                                            <div class="message-body">
                                                <div class="message-row">
                                                    <div class="d-flex align-items-center justify-content-end">

                                                        <div class="message-content bg-primary text-white">
                                                            <div>${message.message}</div>

                                                            <div class="mt-1">
                                                                <small class="opacity-65">${time}</small>
                                                            </div>
                                                        </div>
                                                        <!-- Message: content -->

                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    `
                            else
                                item += `<div class="message">

                                        <a class="avatar avatar-sm mr-4 mr-lg-5" href="#" data-chat-sidebar-toggle="#chat-1-user-profile">
                                            <img class="avatar-img issue_user_img_${message.sender}" src="">
                                        </a>

                                        <div class="message-body">

                                                <div class="message-row">
                                                    <div class="d-flex align-items-center">
                                                        <a class="edit"></span></a>
                                                        <a class="delete"></a>
                                                        

                                                        <!-- Message: content -->
                                                        <div class="message-content bg-light">
                                                            <h6 class="mb-2 issue_user_name_${message.sender}"></h6>
                                                            <div>${message.message}</div>

                                                            <div class="mt-1">
                                                                <small class="opacity-65">${time}</small>
                                                            </div>
                                                        </div>
                                                        
                                                    </div>
                                                </div>
                                                <!-- Message: row -->

                                            </div>
                                            <!-- Message: Body -->
                                        </div>
                                    `

                        }

                        wrapper.innerHTML = item;
                        const issue_user_img = document.getElementsByClassName(`issue_user_img_${message.sender}`);
                        const issue_user_name = document.getElementsByClassName(`issue_user_name_${message.sender}`);
                        var url = `http://127.0.0.1:8000/accounts/profile_api/${message.sender}/`;

                        $.get(url, (data) => {
                            var i;
                            for (i = 0; i < issue_user_img.length; i++) {
                                issue_user_img[i].src = data.profile_pic;
                                issue_user_name[i].innerHTML = data.first_name + " " + data.last_name;
                            }
                        })
                    }
                }
                this.ScrollToEnd();
            } else {
                this.newChatSubmit();
            }
        });
        this.buildIssue();
    }

    newChatSubmit = async () => {
        await
        firebase
            .firestore()
            .collection('issues')
            .doc(this.issue_id)
            .set({
                messages: [{
                    message: "hi",
                    sender: this.sender_id,
                    timestamp: Date.now()
                }],
                issue: this.issue_id
            })
    }

    ScrollToEnd = () => {

        const container = document.getElementById('chatview-container');
        if (container)
            container.scrollTo(0, container.scrollHeight);
    }

}

class Projectchat {

    initialize(projectid, senderid) {
        this.isactive = true
        this.project_id = String(projectid);
        this.sender_id = senderid;
        this.search_message = "";
        this.loadchat();
    }

    loadchat() {
        if (SelectedChatDiv.classList.contains('hide')) {
            SelectedChatDiv.classList.remove('hide');
            NoChatDiv.classList.add('hide');
        }
        this.buildchat();
    }

    sendMessage = async (msg) => {
        if (msg != "") {
            await
            firebase
                .firestore()
                .collection('projects')
                .doc(this.project_id)
                .update({
                    messages: firebase.firestore.FieldValue.arrayUnion({
                        sender: this.sender_id,
                        message: msg,
                        timestamp: Date.now()
                    }),
                });
        }
    }

    buildProject() {

        const ProfilePic = document.getElementById('chat_instance_profile_pic');
        const ProfileName = document.getElementById(`chat_instance_profile_name`);
        const ProfileSkills = document.getElementById('userskills');

        var url = `http://127.0.0.1:8000/projects/project_detail_api/${this.project_id}/`;
        $.get(url, (data) => {

            ProfilePic.src = `https://picsum.photos/id/${this.project_id}/200/300`;
            ProfileName.innerHTML = data.name;
            ProfileSkills.innerHTML = "Deadline " + data.deadline + " | Priority " + data.priority;
        })
    }

    searchfunc = async (e) => {
        this.search_message = e;
        this.buildchat();
    }

    buildchat = async () => {
        const firebaseRef = firebase.firestore().collection('projects').doc(this.project_id);

        firebaseRef.onSnapshot((value) => {
            if (typeof value.data() != "undefined") {

                //var filterArray = value.data().users.filter(_user => _user == this.user_id)[0].split('')[0];

                this.messages = value.data().messages;
                var message;
                var item = "";

                if (this.project_id == value.data().project && this.isactive) {
                    for (message of this.messages) {
                        const time = moment(message.timestamp).fromNow();
                        if (this.search_message !== "" && message.message.indexOf(this.search_message) === -1) {} else {

                            if (message.sender == this.sender_id)
                                item += `<div class="message message-right">
                                            <div class="message-body">
                                                <div class="message-row">
                                                    <div class="d-flex align-items-center justify-content-end">

                                                        <div class="message-content bg-primary text-white">
                                                            <div>${message.message}</div>

                                                            <div class="mt-1">
                                                                <small class="opacity-65">${time}</small>
                                                            </div>
                                                        </div>
                                                        <!-- Message: content -->

                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    `
                            else
                                item += `<div class="message">

                                        <a class="avatar avatar-sm mr-4 mr-lg-5" href="#" data-chat-sidebar-toggle="#chat-1-user-profile">
                                            <img class="avatar-img project_user_img_${message.sender}" src="">
                                        </a>

                                        <div class="message-body">

                                                <div class="message-row">
                                                    <div class="d-flex align-items-center">
                                                        <a class="edit"></span></a>
                                                        <a class="delete"></a>
                                                        

                                                        <!-- Message: content -->
                                                        <div class="message-content bg-light">
                                                            <h6 class="mb-2 project_user_name_${message.sender}"></h6>
                                                            <div>${message.message}</div>

                                                            <div class="mt-1">
                                                                <small class="opacity-65">${time}</small>
                                                            </div>
                                                        </div>
                                                        
                                                    </div>
                                                </div>
                                                <!-- Message: row -->

                                            </div>
                                            <!-- Message: Body -->
                                        </div>
                                    `

                        }

                        wrapper.innerHTML = item;
                        const project_user_img = document.getElementsByClassName(`project_user_img_${message.sender}`);
                        const project_user_name = document.getElementsByClassName(`project_user_name_${message.sender}`);
                        var url = `http://127.0.0.1:8000/accounts/profile_api/${message.sender}/`;

                        $.get(url, (data) => {
                            var i;
                            for (i = 0; i < project_user_img.length; i++) {
                                project_user_img[i].src = data.profile_pic;
                                project_user_name[i].innerHTML = data.first_name + " " + data.last_name;
                            }
                        })
                    }
                }
                this.ScrollToEnd();
            } else {
                this.newChatSubmit();
            }
        });
        this.buildProject();
    }

    newChatSubmit = async () => {
        await
        firebase
            .firestore()
            .collection('projects')
            .doc(this.project_id)
            .set({
                messages: [{
                    message: "hi",
                    sender: this.sender_id,
                    timestamp: Date.now()
                }],
                project: this.project_id
            })
    }

    ScrollToEnd = () => {

        const container = document.getElementById('chatview-container');
        if (container)
            container.scrollTo(0, container.scrollHeight);
    }

}

var chat_instance = new chat;
var issue_instance = new Issuechat;
var project_instance = new Projectchat;


SortObject = (a, b) => {
    const bandA = a.messages[a.messages.length - 1].timestamp;
    const bandB = b.messages[b.messages.length - 1].timestamp;
    let comparison = 0;
    if (bandA > bandB) {
        comparison = -1;
    } else if (bandA < bandB) {
        comparison = 1;
    }
    return comparison;
}

ListAllActiveChats = async () => {
    await firebase
        .firestore()
        .collection('chats')
        .where('users', 'array-contains', user)
        .onSnapshot((value) => {
            const chats = value.docs.map(_doc => _doc.data());
            var item = "";
            chats.sort(SortObject);

            chats.map((_chat, _index) => {
                const lastmessage = _chat.messages[_chat.messages.length - 1].message.substring(0, 20);
                const time = moment(_chat.messages[_chat.messages.length - 1].timestamp).fromNow();
                const secondUser = _chat.users.filter(_user => _user !== user)[0].split('')[0];

                item += `<a onclick="newchat(${secondUser},${user})" class="text-reset nav-link p-0 mb-6">
                            <div id="cardbody_${secondUser}" class="card card-active-listener">
                                <div class="card-body">
                                    <div class="media">
                                        
                                        <div class="avatar mr-5">
                                            <img id="profile_pic_${secondUser}" src="" class="avatar-img" 
                                                alt="Bootstrap Themes">
                                        </div>
                        
                                        <div class="media-body overflow-hidden">
                                            <div class="d-flex align-items-center mb-1">
                                                <h6 id="profile_name_${secondUser}" class="text-truncate mb-0 mr-auto">
                                                    </h6>
                                                <p class="small text-muted text-nowrap ml-4">
                                                    ${time}</p>
                                            </div>
                                            <div class="text-truncate">${lastmessage}</div>
                                        </div>
                                    </div>
                        
                                </div>
                            </div>
                            </div>
                        </a> 
                        `

                var url = `http://127.0.0.1:8000/accounts/profile_api/${secondUser}/`;
                $.get(url, (data) => {
                    const profileimg = document.getElementById(`profile_pic_${secondUser}`);
                    const profilename = document.getElementById(`profile_name_${secondUser}`);
                    profileimg.src = data.profile_pic;
                    profilename.innerHTML = data.first_name + " " + data.last_name;

                    if (_chat.receiverHasRead === false && _chat.messages[_chat.messages.length - 1].sender != user && ActiveChatReturn() != secondUser) {
                        const getspan = document.getElementById(`cardbody_${secondUser}`);
                        getspan.innerHTML += `
                        <div class="badge badge-circle badge-primary badge-border-light badge-top-right">
                        <span>!</span>`;
                    }
                })

            });
            chatList.innerHTML = item;
        })
}

ListAllIssues = async () => {
    var i;

    for (i = 0; i < IssueTime.length; i++) {
        const ThisIssueLastMessage = IssueLastMessage[i];
        const ThisIssueTime = IssueTime[i];
        const id = ThisIssueTime.id;
        const firebaseRef = firebase.firestore().collection('issues').doc(id);
        firebaseRef.onSnapshot((value) => {

            const messages = value.data().messages;
            const lastissuemessage = messages[messages.length - 1];
            const LastMessageTimestamp = moment(lastissuemessage.timestamp).fromNow();
            ThisIssueLastMessage.innerHTML = lastissuemessage.message.substring(0, 20);
            ThisIssueTime.innerHTML = LastMessageTimestamp;
        })
    }
}

ListAllProjects = async () => {
    var i;

    for (i = 0; i < ProjectTime.length; i++) {
        const ThisProjectLastMessage = ProjectLastMessage[i];
        const ThisProjectTime = ProjectTime[i];
        const id = ThisProjectTime.id;
        const firebaseRef = firebase.firestore().collection('projects').doc(id);
        firebaseRef.onSnapshot((value) => {
            const messages = value.data().messages;
            const lastprojectmessage = messages[messages.length - 1];
            const LastMessageTimestamp = moment(lastprojectmessage.timestamp).fromNow();
            ThisProjectLastMessage.innerHTML = lastprojectmessage.message.substring(0, 20);
            ThisProjectTime.innerHTML = LastMessageTimestamp;
        })
    }
}

ListAllProjects();
ListAllActiveChats();
ListAllIssues();


function newchat(user_id, sender_id) {
    Textbox_wrapper.innerHTML = `<div class="form-row align-items-center">
    <div class="col">
        <div class="input-group">

            <!-- Textarea -->
            <input onkeyup="textinstance(event)" id="message_textbox" name="message_textbox"
                class="form-control bg-transparent border-0"
                placeholder="Press  Win + .  for emoji selector" rows="1" data-emoji-input
                data-autosize="true">

        </div>

    </div>

    <!-- Submit button -->
    <div class="col-auto">
        <button  onclick="submitmessage()" id="submit" class="btn btn-ico btn-primary rounded-circle">
            <span class="fe-send"></span>
        </button>
    </div>

</div>
`

    chat_instance.initialize(user_id, sender_id);
    issue_instance.isactive = false;
    project_instance.isactive = false;
    const firebaseRef = firebase.firestore().collection('chats').doc(chat_instance.buildDockey());
    firebaseRef.update({
        receiverHasRead: true
    })
}

function textinstance(event) {
    if (event.key === 'Enter') {
        chat_instance.sendMessage(event.target.value);
        event.target.value = "";
    }
}

function OnchangeChats(e) {
    chat_instance.searchfunc(e.target.value);
}

function submitmessage() {
    const TextBox = document.getElementById('message_textbox');
    chat_instance.sendMessage(TextBox.value);
    TextBox.value = "";
}

function ActiveChatReturn() {
    let id = chat_instance.user_id;
    return (id);
}










function IssueNewChat(issue_id, sender_id) {

    issue_instance.initialize(issue_id, sender_id);
    project_instance.isactive = false;
    chat_instance.isactive = false;
    Textbox_wrapper.innerHTML = `<div class="form-row align-items-center">
    <div class="col">
        <div class="input-group">

            <!-- Textarea -->
            <input onkeyup="Issuetextinstance(event)" id="issue_message_textbox" name="message_textbox"
                class="form-control bg-transparent border-0"
                placeholder="Press  Win + .  for emoji selector" rows="1" data-emoji-input
                data-autosize="true">


            

        </div>

    </div>

    <!-- Submit button -->
    <div class="col-auto">
        <button  onclick="submitissuemessage()" id="submit" class="btn btn-ico btn-primary rounded-circle">
            <span class="fe-send"></span>
        </button>
    </div>

</div>
`
}

function Issuetextinstance(event) {
    if (event.key === 'Enter') {
        issue_instance.sendMessage(event.target.value);
        event.target.value = "";
    }
}

function OnchangeIssues(e) {

    issue_instance.searchfunc(e.target.value);
}

function submitissuemessage() {
    const IssueTextBox = document.getElementById('issue_message_textbox');
    issue_instance.sendMessage(IssueTextBox.value);
    IssueTextBox.value = "";
}

















function ProjectNewChat(project_id, sender_id) {

    project_instance.initialize(project_id, sender_id);
    issue_instance.isactive = false;
    chat_instance.isactive = false;
    Textbox_wrapper.innerHTML = `<div class="form-row align-items-center">
    <div class="col">
        <div class="input-group">

            <!-- Textarea -->
            <input onkeyup="Projecttextinstance(event)" id="project_message_textbox" name="message_textbox"
                class="form-control bg-transparent border-0"
                placeholder="Press  Win + .  for emoji selector" rows="1" data-emoji-input
                data-autosize="true">


            

        </div>

    </div>

    <!-- Submit button -->
    <div class="col-auto">
        <button onclick="submitprojectmessage()" class="btn btn-ico btn-primary rounded-circle">
            <span class="fe-send"></span>
        </button>
    </div>

</div>
`
}

function Projecttextinstance(event) {
    if (event.key === 'Enter') {
        project_instance.sendMessage(event.target.value);
        event.target.value = "";
    }
}

function OnchangeProjects(e) {

    project_instance.searchfunc(e.target.value);
}

function submitprojectmessage() {
    const ProjectTextBox = document.getElementById('project_message_textbox');
    project_instance.sendMessage(ProjectTextBox.value);
    ProjectTextBox.value = "";
}

function TriggerOnChange(e) {
    if (chat_instance.isactive)
        OnchangeChats(e);
    else
    if (issue_instance.isactive)
        OnchangeIssues(e);
    else
    if (project_instance.isactive)
        OnchangeProjects(e);
}