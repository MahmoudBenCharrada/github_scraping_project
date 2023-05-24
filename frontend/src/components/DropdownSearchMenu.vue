<template>
    <div>
        <h2>User Repositories</h2>
        <div class="dropdown">
            <button @click="myFunction()" class="dropbtn">{{ selectedUser }}</button>
            <div id="myDropdown" class="dropdown-content" v-show="showDropDown">
                <input class="inputClass" type="text" placeholder="Search.." id="searchQuery" v-model="searchQuery" @keyup="filterFunction()">
                <ul>
                  <a v-for="item in filteredUsers" :key="item.user_id" @click="filterRepos(item)">{{ item.username }}</a>
                </ul>
            </div>
        </div>
        <ul v-if="filteredRepos">
          <a v-for="item in filteredRepos" :key="item.repo_id" :href="item.url"><li>{{ item.name }}</li></a>
        </ul> 
    </div>
</template>

<script>
export default {
  props: {
    users: {
      type: Array,
      required: true
    },
    repos: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      searchQuery: '',
      filteredUsers: [],
      filteredRepos: [],
      showDropDown: false,
      selectedUser: "Select User"
    }
  },
  mounted() {
      this.filteredUsers = this.users;
  },
  methods: {
    myFunction() {
      this.showDropDown = true
      document.getElementById("myDropdown").classList.toggle("show");
    },
    filterFunction() {
      this.filteredUsers = this.users.filter(user => user.username.toLowerCase().includes(this.searchQuery.toLowerCase()))
    },
    filterRepos(user) {
      this.filteredRepos = this.repos.filter(repo => repo.repo_owner == user.user_id);
      this.selectedUser = user.username
      this.showDropDown = false
    }
  }
}
</script>

<style>
.dropbtn {
  background-color: #04AA6D;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  width: 300px;
}

.dropbtn:hover, .dropbtn:focus {
  background-color: #3e8e41;
}

#myInput {
  box-sizing: border-box;
  background-position: 14px 12px;
  background-repeat: no-repeat;
  font-size: 16px;
  padding: 14px 20px 12px 45px;
  border: none;
  border-bottom: 1px solid #ddd;
}

#myInput:focus {outline: 3px solid #ddd;}

.inputClass {
  width: 290px;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f6f6f6;
  width: 300px;
  overflow: auto;
  border: 1px solid #ddd;
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown a:hover {background-color: #ddd;}

.show {display: block;}

body {
	font-family: 'Gloria Hallelujah', cursive;
	font-size: 1.4rem;
	background: whitesmoke;
	margin: 0;
	padding: 1rem;
	display: grid;
	place-items: center;
	min-height: 100vh;
}

</style>

