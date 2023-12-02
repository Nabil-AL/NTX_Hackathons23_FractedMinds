# **************************************************************************** #
# 	Makefile based on clemedon's Makefile tutorial							   #
# **************************************************************************** #

NAME		:= a.out

# **************************************************************************** #
# 	SOURCES																	   #
# **************************************************************************** #

SRC_DIR		:= src
SRCS		:= \
				main.cpp
SRCS		:= $(addprefix $(SRC_DIR)/,$(SRCS))

INCS		:=	include

BUILD_DIR	:= .build
OBJS		:= $(SRCS:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)
DEPS		:= $(OBJS:.o=.d)

# **************************************************************************** #
# 	LIBRARIES																   #
# **************************************************************************** #

LIB_DIR		:= $(dir $(abspath $(firstword $(MAKEFILE_LIST))))lib
LIBS		:= SDL2
LIB_TARGETS	:= SDL2/build/libsdl.a
LIB_TARGETS	:= $(addprefix $(LIB_DIR)/,$(LIB_TARGETS))
LIB_INCS	:= SDL2/include
INCS		+= $(addprefix $(LIB_DIR)/,$(LIB_INCS))

# **************************************************************************** #
# 	COMPILATION																   #
# **************************************************************************** #

CXX			:= g++
CXXFLAGS	:= -Wall -Wextra -Werror
CPPFLAGS	:= $(addprefix -I,$(INCS)) -MMD -MP
LDFLAGS		:= $(addprefix -L,$(dir $(LIB_TARGETS)))
LDLIBS		:= $(addprefix -l,$(LIBS))
AR			:= ar -rcs

# **************************************************************************** #
# 	UTILITIES																   #
# **************************************************************************** #

RM			:= rm -rf
MAKEFLAGS   += --no-print-directory
DIR_DUP		= @mkdir -p $(@D)

# **************************************************************************** #
# 	RECIPIES :D																   #
# **************************************************************************** #

all: $(NAME)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(DIR_DUP)
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c $< -o $@

$(NAME): $(LIB_TARGETS) $(OBJS)
	$(CXX) $(LDFLAGS) $(OBJS) $(LDLIBS) -o $(NAME)

-include $(DEPS)

clean:
	$(RM) $(OBJS) $(DEPS)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re

# **************************************************************************** #
# 	DEPENDENCIES :3															   #
# **************************************************************************** #

$(LIB_DIR):
	@mkdir -p $(LIB_DIR)

.SECONDEXPANSION:
$(LIB_TARGETS): $(LIB_DIR)/%.a: | $(LIB_DIR)/$$(dir %.a)
	make LIB_DIR=$(LIB_DIR) -C $(dir $@)
