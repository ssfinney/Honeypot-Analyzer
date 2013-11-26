
# This controller needs to be updated with examples from
# both the RFZ2 example and the Devise example found at URL:
# http://railsapps.github.io/

class UsersController < ApplicationController
  respond_to :html

  def index
    @users = User.all
  end

  def new
    @user = User.new
  end

  def create
    @user = User.new(params[:user])
    @user.save
    respond_with @user
  end

  def show
    @user = User.find(params[:id])
  end
end

