<template>
  <div>
    <ul>
      <li v-for="item in users" :key="item.user_id">{{ item.username }}</li>
    </ul>
    <ul>
      <li v-for="item in repos" :key="item.repo_id">{{ item.name }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      repos: []
    };
  },
  async mounted() {
    this.users = await this.fetchData('/users');
    this.repos = await this.fetchData('/repos');
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
