<template>
  <div class="contest-problem-list-card font-bold">
    <div class="table">
      <b-table
        hover
        :items="contestProblems"
        :fields="contestProblemListFields"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
        @row-clicked="goContestProblem"
      >
        <template #cell(title)="data">
          {{data.value}}
          <b-icon
            icon="check2-circle"
            style="color: #8DC63F;"
            font-scale="1.2"
            v-if="data.item.my_status===0"></b-icon>
        </template>
      </b-table>
    </div>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="contestProblems.length"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { types } from '@/store'
import { ProblemMixin } from '@oj/components/mixins'

export default {
  name: 'ContestProblemList',
  components: {
  },
  mixins: [ProblemMixin],
  data () {
    return {
      // ACMTableColumns: [
      //   {
      //     label: '#',
      //     key: 'id',
      //     sortType: 'asc',
      //     width: 150
      //   },
      //   {
      //     label: this.$i18n.t('m.Title'),
      //     key: 'title'
      //   }
      // ],
      contestID: '',
      contest: {},
      contestProblems: [],
      contestProblemListFields: [
        {
          label: '#',
          key: '_id'
        },
        {
          label: 'Title',
          key: 'title'
        }
      ]
    }
  },
  async mounted () {
    this.contestID = this.$route.params.contestID
    this.route_name = this.$route.name
    this.getContestProblems()
    try {
      const res = await this.$store.dispatch('getContest')
      this.changeDomTitle({ title: res.data.data.title })
      const data = res.data.data
      this.contest = data
    } catch (err) {
    }
  },
  methods: {
    async getContestProblems () {
      try {
        const res = await this.$store.dispatch('getContestProblems')
        const data = res.data.data
        this.contestProblems = data
      } catch (err) {
      }
    },
    async goContestProblem (row) {
      await this.$router.push({
        name: 'contest-problem-details',
        params: {
          contestID: this.$route.params.contestID,
          problemID: row._id
        }
      })
    },
    ...mapActions(['changeDomTitle']),
    async handleRoute (route) {
      await this.$router.push(route)
    }
  },
  computed: {
    ...mapState({
      contest: state => state.contest.contest,
      problems: state => state.contest.contestProblems,
      now: state => state.contest.now
    })
  },
  watch: {
    '$route' (newVal) {
      this.route_name = newVal.name
      this.contestID = newVal.params.contestID
      this.changeDomTitle({ title: this.contest.title })
    }
  },
  beforeDestroy () {
    clearInterval(this.timer)
    this.$store.commit(types.CLEAR_CONTEST)
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .table {
    cursor: pointer;
  }
  div {
    &.pagination{
      margin-right: 5%;
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>