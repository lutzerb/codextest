const { createApp } = Vue;

createApp({
  data() {
    return {
      accounts: [],
      entries: [],
      newEntry: {
        debit_id: '',
        credit_id: '',
        amount: '',
        description: ''
      }
    };
  },
  methods: {
    fetchAccounts() {
      axios.get('/api/accounts').then(res => {
        this.accounts = res.data;
      });
    },
    fetchEntries() {
      axios.get('/api/entries').then(res => {
        this.entries = res.data;
      });
    },
    addEntry() {
      axios.post('/api/entries', this.newEntry).then(() => {
        this.fetchEntries();
        this.newEntry = { debit_id: '', credit_id: '', amount: '', description: '' };
      });
    }
  },
  mounted() {
    this.fetchAccounts();
    this.fetchEntries();
  }
}).mount('#app');
