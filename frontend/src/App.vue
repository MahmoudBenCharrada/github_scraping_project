<template>
  <div>
    <DropDownMenu v-if="dataLoaded" :users=users :repos=repos />
  </div>
</template>

<script>
import DropDownMenu from './components/DropdownSearchMenu.vue'
export default {
  components: {
    DropDownMenu
  },
  data() {
    return {
      users: [],
      repos: [],
      dataLoaded: false
    };
  },
  async mounted() {
    this.users = await this.fetchData('/users');
    this.repos = await this.fetchData('/repos');
    this.dataLoaded = true;
  },
  methods: {
    async fetchData(pathName) {
      const url = new URL('http://127.0.0.1:8000');
      url.pathname = pathName;
      const response = await fetch(url);
      return response.json();
    }
  }
};
</script>