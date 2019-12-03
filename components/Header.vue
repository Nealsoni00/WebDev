<template>
  <header>
    <b-navbar type="dark" variant="info">
      <b-navbar-brand>CS376 Final Project - Twitter</b-navbar-brand>
      <b-nav-form class="nav-search-form">
        <b-form-input
          size="sm"
          class="mr-sm-2 search-form"
          placeholder="Search"
        ></b-form-input>
        <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
      </b-nav-form>
    </b-navbar>
  </header>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style lang="scss" scoped>
header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;

  .nav-search-form {
    width: 50%;
    display: flex;
    justify-content: center;

    .search-form {
      width: 300px;
      max-width: 90%;
    }
  }
}
</style>
