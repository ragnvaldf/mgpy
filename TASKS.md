| Status | Feature | Provides | Description | Caveat |
|:------:|---------|----------|-------------|--------|
| <ul><li>- [ ] </li></ul> | Singleton action | Provides a singleton instance | Runs once after requirements are satisfied | Any action requiring it will receive the same instance
| <ul><li>- [ ] </li></ul> | Producer action | Provides new instances until generator returns, or function returns None | Runs at most once | Requirements can only be singletons
| <ul><li>- [ ] </li></ul> | Aggregator action | Provides a singleton instance | Runs at most once with aggregation performed on full producer action output | One requirement must be a producer which aggregation is performed on. Can optionally require singletons
| <ul><li>- [x] </li></ul> | Function action | Provides new instances every time requirements are satisfied | Run at most n times when requirements are satisfied | Amount of requirement instances should be equal (except for singletons)
| <ul><li>- [ ] </li></ul> | ConsumerProducer action | Provides new instances every time requirements are satisfied |  | Amount of requirement instances should be equal (except for singletons)
| <ul><li>- [ ] </li></ul> | Timed action | Provides new instances at most every n seconds | Run at most every n seconds when requirements are satisfied | Amount of requirement instances should be equal (except for singletons)
| <ul><li>- [ ] </li></ul> | Mapper action property | In order list of parent action products | Repeat action with each item in a iterable requirement as a parameter | Amount of other requirement instances should be equal (except for singletons). Must map on an action providing an iterable.
| <ul><li>- [ ] </li></ul> | Dynamic profiling | | Functions with iterable requirements and no side effects are run multiple times in different configurations so that the optimal configuration can be selected next time |
